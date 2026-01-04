export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

export const API_ENDPOINTS = {
  auth: {
    register: '/api/auth/register',
    login: '/api/auth/login',
    me: '/api/auth/me',
  },
  movies: {
    list: '/api/movies',
    get: (id) => `/api/movies/${id}`,
    recommendations: '/api/movies/recommendations/me',
    similar: (id) => `/api/movies/${id}/similar`,
  },
  rooms: {
    list: '/api/rooms',
    create: '/api/rooms',
    get: (id) => `/api/rooms/${id}`,
    join: (id) => `/api/rooms/${id}/join`,
    leave: (id) => `/api/rooms/${id}/leave`,
    myRooms: '/api/rooms/my-rooms',
    invite: (id) => `/api/rooms/${id}/invite`,
  },
  reviews: {
    create: '/api/reviews',
    list: '/api/reviews',
    byMovie: (id) => `/api/reviews/movie/${id}`,
    byUser: (id) => `/api/reviews/user/${id}`,
    myReviews: '/api/reviews/me',
    update: (id) => `/api/reviews/${id}`,
    delete: (id) => `/api/reviews/${id}`,
  },
  users: {
    get: (id) => `/api/users/${id}`,
    update: '/api/users/me',
    preferences: '/api/users/me/preferences',
    apiKey: '/api/users/me/api-key',
  },
  tmdb: {
    search: '/api/tmdb/search',
    popular: '/api/tmdb/popular',
    topRated: '/api/tmdb/top-rated',
    import: (id) => `/api/tmdb/import/${id}`,
  },
};

