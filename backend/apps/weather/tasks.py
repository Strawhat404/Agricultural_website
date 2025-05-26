from celery import shared_task
from django.utils import timezone
from django.conf import settings
import requests
from .models import WeatherData, WeatherForecast, WeatherAlert

@shared_task
def update_weather_data():
    """Update weather data for all locations"""
    try:
        # Get all unique locations from the database
        locations = WeatherData.objects.values_list('location', flat=True).distinct()
        
        for location in locations:
            try:
                # Fetch current weather data
                api_key = settings.WEATHER_API_KEY
                url = f'http://api.openweathermap.org/data/2.5/weather'
                params = {
                    'q': location,
                    'appid': api_key,
                    'units': 'metric'
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # Create or update weather data
                WeatherData.objects.create(
                    location=location,
                    latitude=data['coord']['lat'],
                    longitude=data['coord']['lon'],
                    temperature=data['main']['temp'],
                    humidity=data['main']['humidity'],
                    wind_speed=data['wind']['speed'],
                    wind_direction=data['wind'].get('deg', ''),
                    pressure=data['main']['pressure'],
                    precipitation=data.get('rain', {}).get('1h', 0),
                    weather_condition=data['weather'][0]['main'],
                    weather_icon=data['weather'][0]['icon'],
                    timestamp=timezone.now()
                )

            except requests.RequestException as e:
                print(f"Error updating weather data for {location}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in update_weather_data task: {str(e)}")

@shared_task
def update_weather_forecasts():
    """Update weather forecasts for all locations"""
    try:
        # Get all unique locations from the database
        locations = WeatherForecast.objects.values_list('location', flat=True).distinct()
        
        for location in locations:
            try:
                # Fetch forecast data
                api_key = settings.WEATHER_API_KEY
                url = f'http://api.openweathermap.org/data/2.5/forecast'
                params = {
                    'q': location,
                    'appid': api_key,
                    'units': 'metric'
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # Process and store forecast data
                for item in data['list']:
                    forecast_date = timezone.datetime.fromtimestamp(
                        item['dt']
                    ).date()
                    
                    if not WeatherForecast.objects.filter(
                        location=location,
                        forecast_date=forecast_date
                    ).exists():
                        WeatherForecast.objects.create(
                            location=location,
                            latitude=data['city']['coord']['lat'],
                            longitude=data['city']['coord']['lon'],
                            forecast_date=forecast_date,
                            min_temperature=item['main']['temp_min'],
                            max_temperature=item['main']['temp_max'],
                            humidity=item['main']['humidity'],
                            wind_speed=item['wind']['speed'],
                            precipitation_probability=item.get('pop', 0) * 100,
                            weather_condition=item['weather'][0]['main'],
                            weather_icon=item['weather'][0]['icon']
                        )

            except requests.RequestException as e:
                print(f"Error updating forecast data for {location}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in update_weather_forecasts task: {str(e)}")

@shared_task
def check_weather_alerts():
    """Check for weather alerts and update their status"""
    try:
        # Update expired alerts
        WeatherAlert.objects.filter(
            is_active=True,
            end_time__lt=timezone.now()
        ).update(is_active=False)

        # Get all unique locations from the database
        locations = WeatherAlert.objects.values_list('location', flat=True).distinct()
        
        for location in locations:
            try:
                # Fetch weather alerts
                api_key = settings.WEATHER_API_KEY
                url = f'http://api.openweathermap.org/data/2.5/onecall'
                params = {
                    'lat': WeatherData.objects.filter(location=location).first().latitude,
                    'lon': WeatherData.objects.filter(location=location).first().longitude,
                    'appid': api_key,
                    'exclude': 'current,minutely,hourly,daily'
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # Process and store alert data
                if 'alerts' in data:
                    for alert in data['alerts']:
                        if not WeatherAlert.objects.filter(
                            location=location,
                            alert_type=alert['event'],
                            start_time=timezone.datetime.fromtimestamp(alert['start']),
                            end_time=timezone.datetime.fromtimestamp(alert['end'])
                        ).exists():
                            WeatherAlert.objects.create(
                                location=location,
                                alert_type=alert['event'],
                                severity='high' if alert.get('severity') == 'Extreme' else 'moderate',
                                description=alert['description'],
                                start_time=timezone.datetime.fromtimestamp(alert['start']),
                                end_time=timezone.datetime.fromtimestamp(alert['end']),
                                is_active=True
                            )

            except requests.RequestException as e:
                print(f"Error checking weather alerts for {location}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in check_weather_alerts task: {str(e)}") 