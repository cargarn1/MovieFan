import api from './api';
import { API_ENDPOINTS } from '../config';

export const reviewsService = {
  async create(reviewData) {
    const response = await api.post(API_ENDPOINTS.reviews.create, reviewData);
    return response.data;
  },

  async getByMovie(movieId, params = {}) {
    const response = await api.get(API_ENDPOINTS.reviews.byMovie(movieId), { params });
    return response.data;
  },

  async getMyReviews(params = {}) {
    const response = await api.get(API_ENDPOINTS.reviews.myReviews, { params });
    return response.data;
  },

  async update(id, reviewData) {
    const response = await api.put(API_ENDPOINTS.reviews.update(id), reviewData);
    return response.data;
  },

  async delete(id) {
    await api.delete(API_ENDPOINTS.reviews.delete(id));
  },
};



