import api from './api';
import { API_ENDPOINTS } from '../config';

export const usersService = {
  async get(id) {
    const response = await api.get(API_ENDPOINTS.users.get(id));
    return response.data;
  },

  async update(userData) {
    const response = await api.put(API_ENDPOINTS.users.update, userData);
    return response.data;
  },

  async getPreferences() {
    const response = await api.get(API_ENDPOINTS.users.preferences);
    return response.data;
  },

  async updatePreferences(preferences) {
    const response = await api.put(API_ENDPOINTS.users.preferences, preferences);
    return response.data;
  },

  async getApiKey() {
    const response = await api.get(API_ENDPOINTS.users.apiKey);
    return response.data;
  },
};

