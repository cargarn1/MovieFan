import api from './api';
import { API_ENDPOINTS } from '../config';

export const authService = {
  async register(userData) {
    const response = await api.post(API_ENDPOINTS.auth.register, userData);
    return response.data;
  },

  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post(API_ENDPOINTS.auth.login, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get(API_ENDPOINTS.auth.me);
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },
};

