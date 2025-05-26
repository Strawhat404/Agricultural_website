import axios from 'axios';
import { API_BASE_URL } from '../config';

const authApi = axios.create({
    baseURL: `${API_BASE_URL}/auth`,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface LoginCredentials {
    username: string;
    password: string;
}

export const authService = {
    login: async (credentials: LoginCredentials) => {
        const response = await authApi.post('/login/', credentials);
        const { token } = response.data;
        localStorage.setItem('token', token);
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },
}; 