import axios from 'axios';
import { API_BASE_URL } from '../config';

const weatherApi = axios.create({
    baseURL: `${API_BASE_URL}/weather`,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
});

export interface WeatherData {
    id: number;
    location: string;
    latitude: number;
    longitude: number;
    temperature: number;
    humidity: number;
    wind_speed: number;
    wind_direction: string;
    precipitation: number;
    pressure: number;
    weather_condition: string;
    weather_icon: string;
    timestamp: string;
    created_at: string;
}

export interface WeatherForecast {
    id: number;
    location: string;
    latitude: number;
    longitude: number;
    forecast_date: string;
    min_temperature: number;
    max_temperature: number;
    humidity: number;
    wind_speed: number;
    precipitation_probability: number;
    weather_condition: string;
    weather_icon: string;
    created_at: string;
}

export interface WeatherAlert {
    id: string;
    location: string;
    alert_type: string;
    severity: string;
    description: string;
    start_time: string;
    end_time: string;
    is_active: boolean;
    created_at: string;
    title: string;
    valid_until: string;
    source: string;
}

export const weatherService = {
    getCurrentWeather: async (location: string): Promise<WeatherData> => {
        const response = await weatherApi.get(`/data/current/?location=${encodeURIComponent(location)}`);
        return response.data;
    },

    getWeatherForecast: async (location: string): Promise<WeatherForecast[]> => {
        const response = await weatherApi.get(`/forecast/forecast/?location=${encodeURIComponent(location)}`);
        return response.data;
    },

    getActiveAlerts: async (location: string): Promise<WeatherAlert[]> => {
        const response = await weatherApi.get(`/alerts/active/?location=${encodeURIComponent(location)}`);
        return response.data;
    },

    getAllAlerts: async (): Promise<WeatherAlert[]> => {
        const response = await weatherApi.get('/alerts/');
        return response.data;
    },
}; 