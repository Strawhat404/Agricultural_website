from rest_framework import serializers
from .models import WeatherData, WeatherForecast, WeatherAlert

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'id', 'location', 'latitude', 'longitude',
            'temperature', 'humidity', 'wind_speed',
            'wind_direction', 'precipitation', 'pressure',
            'weather_condition', 'weather_icon', 'timestamp',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = [
            'id', 'location', 'latitude', 'longitude',
            'forecast_date', 'min_temperature', 'max_temperature',
            'humidity', 'wind_speed', 'precipitation_probability',
            'weather_condition', 'weather_icon', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class WeatherAlertSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = WeatherAlert
        fields = [
            'id', 'location', 'alert_type', 'severity',
            'severity_display', 'description', 'start_time',
            'end_time', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at'] 