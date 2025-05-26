import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { weatherService, WeatherForecast as WeatherForecastType } from '../../services/weatherService';
import { format } from 'date-fns';

interface WeatherForecastProps {
    location: string;
}

const WeatherForecast: React.FC<WeatherForecastProps> = ({ location }) => {
    const { data: forecasts, isLoading, error } = useQuery<WeatherForecastType[]>({
        queryKey: ['weatherForecast', location],
        queryFn: () => weatherService.getWeatherForecast(location),
        refetchInterval: 1800000, // Refetch every 30 minutes
    });

    if (isLoading) {
        return (
            <div className="animate-pulse bg-white rounded-lg shadow-md p-6">
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-6"></div>
                <div className="grid grid-cols-5 gap-4">
                    {[...Array(5)].map((_, index) => (
                        <div key={index} className="bg-gray-50 rounded-lg p-4">
                            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                            <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
                            <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 className="text-red-800 font-medium">Error loading forecast data</h3>
                <p className="text-red-600 mt-2">Please try again later</p>
            </div>
        );
    }

    if (!forecasts || forecasts.length === 0) {
        return null;
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">5-Day Forecast</h2>
            <div className="grid grid-cols-5 gap-4">
                {forecasts.slice(0, 5).map((forecast) => (
                    <div key={forecast.id} className="bg-gray-50 rounded-lg p-4 text-center">
                        <p className="text-sm font-medium text-gray-600">
                            {format(new Date(forecast.forecast_date), 'EEE')}
                        </p>
                        <p className="text-xs text-gray-500">
                            {format(new Date(forecast.forecast_date), 'MMM d')}
                        </p>
                        <img
                            src={`http://openweathermap.org/img/wn/${forecast.weather_icon}.png`}
                            alt={forecast.weather_condition}
                            className="w-12 h-12 mx-auto my-2"
                        />
                        <div className="flex justify-center items-center space-x-2">
                            <p className="text-lg font-semibold text-gray-900">
                                {Math.round(forecast.max_temperature)}°
                            </p>
                            <p className="text-sm text-gray-500">
                                {Math.round(forecast.min_temperature)}°
                            </p>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                            {forecast.precipitation_probability}% rain
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WeatherForecast; 