from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'data', views.WeatherDataViewSet, basename='weather-data')
router.register(r'forecast', views.WeatherForecastViewSet, basename='weather-forecast')
router.register(r'alerts', views.WeatherAlertViewSet, basename='weather-alerts')

urlpatterns = [
    path('', include(router.urls)),
] 