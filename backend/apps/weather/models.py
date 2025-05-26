from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class WeatherData(models.Model):
    location = models.CharField(
        max_length=100,
        verbose_name=_('Location')
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_('Longitude')
    )
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_('Temperature (°C)')
    )
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Humidity (%)')
    )
    wind_speed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Wind Speed (m/s)')
    )
    wind_direction = models.CharField(
        max_length=3,
        verbose_name=_('Wind Direction')
    )
    precipitation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Precipitation (mm)')
    )
    pressure = models.IntegerField(
        verbose_name=_('Pressure (hPa)')
    )
    weather_condition = models.CharField(
        max_length=50,
        verbose_name=_('Weather Condition')
    )
    weather_icon = models.CharField(
        max_length=10,
        verbose_name=_('Weather Icon Code')
    )
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    class Meta:
        verbose_name = _('Weather Data')
        verbose_name_plural = _('Weather Data')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.location} - {self.timestamp}"

class WeatherForecast(models.Model):
    location = models.CharField(
        max_length=100,
        verbose_name=_('Location')
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_('Longitude')
    )
    forecast_date = models.DateField(
        verbose_name=_('Forecast Date')
    )
    min_temperature = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_('Min Temperature (°C)')
    )
    max_temperature = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_('Max Temperature (°C)')
    )
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Humidity (%)')
    )
    wind_speed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Wind Speed (m/s)')
    )
    precipitation_probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Precipitation Probability (%)')
    )
    weather_condition = models.CharField(
        max_length=50,
        verbose_name=_('Weather Condition')
    )
    weather_icon = models.CharField(
        max_length=10,
        verbose_name=_('Weather Icon Code')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    class Meta:
        verbose_name = _('Weather Forecast')
        verbose_name_plural = _('Weather Forecasts')
        ordering = ['forecast_date']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['forecast_date']),
        ]

    def __str__(self):
        return f"{self.location} - {self.forecast_date}"

class WeatherAlert(models.Model):
    SEVERITY_CHOICES = (
        ('low', _('Low')),
        ('moderate', _('Moderate')),
        ('high', _('High')),
        ('extreme', _('Extreme')),
    )

    location = models.CharField(
        max_length=100,
        verbose_name=_('Location')
    )
    alert_type = models.CharField(
        max_length=50,
        verbose_name=_('Alert Type')
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        verbose_name=_('Severity')
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    start_time = models.DateTimeField(
        verbose_name=_('Start Time')
    )
    end_time = models.DateTimeField(
        verbose_name=_('End Time')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    class Meta:
        verbose_name = _('Weather Alert')
        verbose_name_plural = _('Weather Alerts')
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.alert_type} - {self.location} ({self.get_severity_display()})" 