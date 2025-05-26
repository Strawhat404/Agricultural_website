import React, { useState } from 'react';
import CurrentWeather from '../components/weather/CurrentWeather';
import WeatherForecast from '../components/weather/WeatherForecast';
import WeatherAlerts from '../components/weather/WeatherAlerts';

const WeatherPage: React.FC = () => {
    const [location, setLocation] = useState<string>('');

    const handleLocationSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const input = form.elements.namedItem('location') as HTMLInputElement;
        if (input.value.trim()) {
            setLocation(input.value.trim());
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Weather Information</h1>
                
                <form onSubmit={handleLocationSubmit} className="mb-8">
                    <div className="flex gap-4">
                        <input
                            type="text"
                            name="location"
                            placeholder="Enter location (e.g., City, Country)"
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            required
                        />
                        <button
                            type="submit"
                            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                        >
                            Get Weather
                        </button>
                    </div>
                </form>

                {location && (
                    <div className="space-y-8">
                        <CurrentWeather location={location} />
                        <WeatherForecast location={location} />
                        <WeatherAlerts location={location} />
                    </div>
                )}

                {!location && (
                    <div className="text-center py-12">
                        <p className="text-gray-600">
                            Enter a location above to view weather information
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default WeatherPage; 