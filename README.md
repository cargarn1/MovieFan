# MovieFan - Movie Recommendation & Social Platform

A social platform where users can create and join rooms based on movie preferences, discuss specific movies, and get personalized recommendations.

## Features

- 🎬 **Movie Rooms**: Create or join rooms centered around specific movies
- 👥 **Social Features**: Invite friends and connect with other movie enthusiasts
- 🎯 **Personalized Recommendations**: Get movie suggestions based on your preferences
- ⭐ **Movie Ratings & Reviews**: Rate and review movies (1-10 scale)
- 🎞️ **TMDB Integration**: Search and import movies from The Movie Database
- 🔐 **User Authentication**: Secure JWT-based authentication system
- 💬 **Room Management**: Join, leave, and manage movie discussion rooms
- 🔌 **Zapier Integration**: Connect with Zapier for automation and webhooks

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (if it exists) or create a `.env` file
   - Add your TMDB API key (get one free at https://www.themoviedb.org/settings/api):
   ```
   TMDB_API_KEY=your_tmdb_api_key_here
   ```
   - Configure other settings as needed (JWT secret, database URL, etc.)

4. Initialize the database:
```bash
python -m app.init_db
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:5001`

API documentation available at `http://localhost:5001/docs`

The frontend will run on `http://localhost:5000`

## Project Structure

```
MovieFan/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── users.py         # User management routes
│   │   ├── movies.py        # Movie routes
│   │   ├── rooms.py         # Room management routes
│   │   ├── reviews.py       # Review/rating routes
│   │   └── tmdb.py          # TMDB integration routes
│   └── services/            # Business logic
│       ├── __init__.py
│       ├── recommendation.py  # Movie recommendation engine
│       ├── room_service.py    # Room management logic
│       └── tmdb_service.py    # TMDB API service
├── requirements.txt
├── README.md
└── .env.example
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Movies
- `GET /api/movies` - List movies (with search/filter)
- `GET /api/movies/{movie_id}` - Get movie details
- `POST /api/movies` - Create a new movie entry
- `GET /api/movies/recommendations/me` - Get personalized recommendations
- `GET /api/movies/{movie_id}/similar` - Get similar movies

### Rooms
- `POST /api/rooms` - Create a new room
- `GET /api/rooms` - List available rooms
- `GET /api/rooms/{room_id}` - Get room details
- `POST /api/rooms/{room_id}/join` - Join a room
- `POST /api/rooms/{room_id}/leave` - Leave a room
- `POST /api/rooms/{room_id}/invite` - Invite user to room
- `GET /api/rooms/my-rooms` - Get user's rooms

### Reviews & Ratings
- `POST /api/reviews` - Create a review/rating for a movie
- `GET /api/reviews/movie/{movie_id}` - Get all reviews for a movie
- `GET /api/reviews/user/{user_id}` - Get all reviews by a user
- `GET /api/reviews/me` - Get current user's reviews
- `GET /api/reviews/{review_id}` - Get a specific review
- `PUT /api/reviews/{review_id}` - Update a review
- `DELETE /api/reviews/{review_id}` - Delete a review

### TMDB Integration
- `GET /api/tmdb/search` - Search movies on TMDB
- `GET /api/tmdb/movie/{tmdb_id}` - Get movie details from TMDB
- `POST /api/tmdb/import/{tmdb_id}` - Import a movie from TMDB
- `GET /api/tmdb/popular` - Get popular movies from TMDB
- `GET /api/tmdb/top-rated` - Get top rated movies from TMDB
- `GET /api/tmdb/upcoming` - Get upcoming movies from TMDB

### Users
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/me/preferences` - Get user preferences
- `PUT /api/users/me/preferences` - Update user preferences
- `GET /api/users/me/api-key` - Get or create API key for Zapier

### Zapier Integration
- `GET /api/zapier/api-key` - Get or create API key
- `GET /api/zapier/test` - Test API connection
- `POST /api/zapier/webhooks` - Create webhook subscription
- `GET /api/zapier/webhooks` - List webhook subscriptions
- `DELETE /api/zapier/webhooks/{id}` - Delete webhook subscription
- `POST /api/zapier/rooms` - Create room (Zapier-friendly)
- `GET /api/zapier/rooms` - List rooms (Zapier-friendly)
- `POST /api/zapier/reviews` - Create review (Zapier-friendly)
- `GET /api/zapier/reviews` - List reviews (Zapier-friendly)
- `GET /api/zapier/movies` - List/search movies (Zapier-friendly)

See [ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md) for detailed Zapier setup guide.

