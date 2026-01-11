import api from './api';
import { API_ENDPOINTS } from '../config';

export const roomsService = {
  async list(params = {}) {
    const response = await api.get(API_ENDPOINTS.rooms.list, { params });
    return response.data;
  },

  async get(id) {
    const response = await api.get(API_ENDPOINTS.rooms.get(id));
    return response.data;
  },

  async create(roomData) {
    const response = await api.post(API_ENDPOINTS.rooms.create, roomData);
    return response.data;
  },

  async join(id) {
    const response = await api.post(API_ENDPOINTS.rooms.join(id));
    return response.data;
  },

  async leave(id) {
    const response = await api.post(API_ENDPOINTS.rooms.leave(id));
    return response.data;
  },

  async getMyRooms() {
    const response = await api.get(API_ENDPOINTS.rooms.myRooms);
    return response.data;
  },

  async invite(roomId, inviteeId, message) {
    const response = await api.post(API_ENDPOINTS.rooms.invite(roomId), {
      room_id: roomId,
      invitee_id: inviteeId,
      message,
    });
    return response.data;
  },
};



