import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { weatherService, WeatherData } from '../../services/weatherService';
import { format } from 'date-fns';

interface CurrentWeatherProps {
    location: string;
}

const CurrentWeather: React.FC<CurrentWeatherProps> = ({ location }) => {
    const { data: weather, isLoading, error } = useQuery<WeatherData>({
        queryKey: ['currentWeather', location],
        queryFn: () => weatherService.getCurrentWeather(location),
        refetchInterval: 300000, // Refetch every 5 minutes
    });

    if (isLoading) {
        return (
            <div className="animate-pulse bg-white rounded-lg shadow-md p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 className="text-red-800 font-medium">Error loading weather data</h3>
                <p className="text-red-600 mt-2">Please try again later</p>
            </div>
        );
    }

    if (!weather) {
        return null;
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-800">{weather.location}</h2>
                <span className="text-sm text-gray-500">
                    {format(new Date(weather.timestamp), 'MMM d, h:mm a')}
                </span>
            </div>
            
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                    <img
                        src={`http://openweathermap.org/img/wn/${weather.weather_icon}@2x.png`}
                        alt={weather.weather_condition}
                        className="w-16 h-16"
                    />
                    <div>
                        <p className="text-4xl font-bold text-gray-900">{Math.round(weather.temperature)}°C</p>
                        <p className="text-gray-600 capitalize">{weather.weather_condition}</p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Humidity</p>
                    <p className="text-lg font-semibold text-gray-900">{weather.humidity}%</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Wind Speed</p>
                    <p className="text-lg font-semibold text-gray-900">{weather.wind_speed} m/s</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Pressure</p>
                    <p className="text-lg font-semibold text-gray-900">{weather.pressure} hPa</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Precipitation</p>
                    <p className="text-lg font-semibold text-gray-900">{weather.precipitation} mm</p>
                </div>
            </div>
        </div>
    );
};

export default CurrentWeather; 