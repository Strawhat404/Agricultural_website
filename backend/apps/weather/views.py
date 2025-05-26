from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
import requests
from .models import WeatherData, WeatherForecast, WeatherAlert
from .serializers import (
    WeatherDataSerializer,
    WeatherForecastSerializer,
    WeatherAlertSerializer
)

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['location', 'timestamp']
    search_fields = ['location']
    ordering_fields = ['timestamp', 'temperature']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current weather data for a location"""
        location = request.query_params.get('location')
        if not location:
            return Response(
                {'error': 'Location parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get cached data first
        weather_data = WeatherData.objects.filter(
            location=location,
            timestamp__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).first()

        if not weather_data:
            # Fetch from OpenWeatherMap API
            try:
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

                weather_data = WeatherData.objects.create(
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
                return Response(
                    {'error': f'Failed to fetch weather data: {str(e)}'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        serializer = self.get_serializer(weather_data)
        return Response(serializer.data)

class WeatherForecastViewSet(viewsets.ModelViewSet):
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['location', 'forecast_date']
    search_fields = ['location']
    ordering_fields = ['forecast_date']
    ordering = ['forecast_date']

    @action(detail=False, methods=['get'])
    def forecast(self, request):
        """Get weather forecast for a location"""
        location = request.query_params.get('location')
        if not location:
            return Response(
                {'error': 'Location parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get cached forecast first
        forecasts = WeatherForecast.objects.filter(
            location=location,
            forecast_date__gte=timezone.now().date()
        ).order_by('forecast_date')

        if not forecasts.exists():
            # Fetch from OpenWeatherMap API
            try:
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

                forecasts = WeatherForecast.objects.filter(
                    location=location,
                    forecast_date__gte=timezone.now().date()
                ).order_by('forecast_date')

            except requests.RequestException as e:
                return Response(
                    {'error': f'Failed to fetch forecast data: {str(e)}'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)

class WeatherAlertViewSet(viewsets.ModelViewSet):
    queryset = WeatherAlert.objects.all()
    serializer_class = WeatherAlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['location', 'alert_type', 'severity', 'is_active']
    search_fields = ['location', 'alert_type']
    ordering_fields = ['start_time', 'severity']
    ordering = ['-start_time']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active weather alerts for a location"""
        location = request.query_params.get('location')
        if not location:
            return Response(
                {'error': 'Location parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        alerts = WeatherAlert.objects.filter(
            location=location,
            is_active=True,
            end_time__gt=timezone.now()
        ).order_by('-start_time')

        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data) 