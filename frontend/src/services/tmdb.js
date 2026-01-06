import api from './api';
import { API_ENDPOINTS } from '../config';

export const tmdbService = {
  async search(query, page = 1) {
    const response = await api.get(API_ENDPOINTS.tmdb.search, {
      params: { query, page },
    });
    return response.data;
  },

  async getPopular(page = 1) {
    const response = await api.get(API_ENDPOINTS.tmdb.popular, {
      params: { page },
    });
    return response.data;
  },

  async getTopRated(page = 1) {
    const response = await api.get(API_ENDPOINTS.tmdb.topRated, {
      params: { page },
    });
    return response.data;
  },

  async importMovie(tmdbId) {
    const response = await api.post(API_ENDPOINTS.tmdb.import(tmdbId));
    return response.data;
  },
};


