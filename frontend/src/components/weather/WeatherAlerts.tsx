import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { weatherService, WeatherAlert as WeatherAlertType } from '../../services/weatherService';
import { format } from 'date-fns';

interface WeatherAlertsProps {
    location: string;
}

const WeatherAlerts: React.FC<WeatherAlertsProps> = ({ location }) => {
    const { data: alerts, isLoading, error } = useQuery<WeatherAlertType[]>({
        queryKey: ['weatherAlerts', location],
        queryFn: () => weatherService.getActiveAlerts(location),
        refetchInterval: 300000, // Refetch every 5 minutes
    });

    if (isLoading) {
        return (
            <div className="animate-pulse bg-white rounded-lg shadow-md p-6">
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                <div className="space-y-4">
                    {[...Array(2)].map((_, index) => (
                        <div key={index} className="bg-gray-50 rounded-lg p-4">
                            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 className="text-red-800 font-medium">Error loading weather alerts</h3>
                <p className="text-red-600 mt-2">Please try again later</p>
            </div>
        );
    }

    if (!alerts || alerts.length === 0) {
        return (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h3 className="text-green-800 font-medium">No Active Weather Alerts</h3>
                <p className="text-green-600 mt-2">Current weather conditions are normal</p>
            </div>
        );
    }

    const getSeverityColor = (severity: string) => {
        switch (severity.toLowerCase()) {
            case 'extreme':
                return 'bg-red-100 border-red-200 text-red-800';
            case 'severe':
                return 'bg-orange-100 border-orange-200 text-orange-800';
            case 'moderate':
                return 'bg-yellow-100 border-yellow-200 text-yellow-800';
            default:
                return 'bg-blue-100 border-blue-200 text-blue-800';
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Weather Alerts</h2>
            <div className="space-y-4">
                {alerts.map((alert) => (
                    <div
                        key={alert.id}
                        className={`border rounded-lg p-4 ${getSeverityColor(alert.severity)}`}
                    >
                        <div className="flex justify-between items-start">
                            <div>
                                <h3 className="font-medium">{alert.title || alert.alert_type}</h3>
                                <p className="text-sm mt-1">{alert.description}</p>
                            </div>
                            <span className="text-xs font-medium px-2 py-1 rounded-full bg-white bg-opacity-50">
                                {alert.severity}
                            </span>
                        </div>
                        <div className="mt-4 text-sm">
                            <p>Valid until: {format(new Date(alert.valid_until || alert.end_time), 'MMM d, yyyy HH:mm')}</p>
                            <p className="mt-1">Source: {alert.source || 'Weather Service'}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WeatherAlerts; 