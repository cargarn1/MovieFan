import api from './api';
import { API_ENDPOINTS } from '../config';

export const moviesService = {
  async list(params = {}) {
    const response = await api.get(API_ENDPOINTS.movies.list, { params });
    return response.data;
  },

  async get(id) {
    const response = await api.get(API_ENDPOINTS.movies.get(id));
    return response.data;
  },

  async getRecommendations() {
    const response = await api.get(API_ENDPOINTS.movies.recommendations);
    return response.data;
  },

  async getSimilar(id) {
    const response = await api.get(API_ENDPOINTS.movies.similar(id));
    return response.data;
  },
};



