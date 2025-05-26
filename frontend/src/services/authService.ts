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

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    password2: string;
    first_name: string;
    last_name: string;
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

    register: async (data: RegisterData) => {
        const response = await axios.post(`${API_BASE_URL}/auth/register/`, data);
        return response.data;
    },
}; 