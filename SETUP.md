# MovieFan Setup Guide

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file in the project root with:
```env
# Database
DATABASE_URL=sqlite:///./moviefan.db

# JWT Secret Key (change this in production!)
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# TMDB API Key (get one free at https://www.themoviedb.org/settings/api)
TMDB_API_KEY=your_tmdb_api_key_here

# Server Port (defaults to 5001 if not set)
PORT=5001
```

3. **Get a TMDB API Key:**
   - Go to https://www.themoviedb.org/
   - Sign up for a free account
   - Go to Settings → API
   - Request an API key (it's free!)
   - Copy the API key to your `.env` file

4. **Initialize the database:**
```bash
python -m app.init_db
```

5. **Run the server:**
```bash
python run.py
# or
uvicorn app.main:app --reload
```

6. **Access the API:**
   - API: http://localhost:5001
   - Interactive Docs: http://localhost:5001/docs
   - Alternative Docs: http://localhost:5001/redoc

## Features Overview

### Movie Ratings & Reviews
- Users can rate movies on a 1-10 scale
- Write detailed reviews
- Movies automatically calculate average ratings
- One review per user per movie

### TMDB Integration
- Search millions of movies from The Movie Database
- Import movies directly into your database
- Browse popular, top-rated, and upcoming movies
- All imported movies include TMDB ID for reference

## Testing the API

### 1. Register a user:
```bash
curl -X POST "http://localhost:5001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Login:
```bash
curl -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### 3. Search TMDB:
```bash
curl "http://localhost:5001/api/tmdb/search?query=inception"
```

### 4. Import a movie (replace TOKEN with your JWT token):
```bash
curl -X POST "http://localhost:5001/api/tmdb/import/27205" \
  -H "Authorization: Bearer TOKEN"
```

### 5. Create a review:
```bash
curl -X POST "http://localhost:5001/api/reviews" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "rating": 9,
    "review_text": "Great movie!"
  }'
```

## Database Schema

The application uses SQLite by default (can be changed to PostgreSQL). Key tables:

- **users**: User accounts
- **movies**: Movie catalog
- **reviews**: User ratings and reviews
- **rooms**: Discussion rooms
- **room_members**: Room membership (many-to-many)
- **invitations**: Room invitations
- **user_preferences**: User movie preferences

## Production Deployment

For production:

1. Change `DATABASE_URL` to PostgreSQL
2. Set a strong `SECRET_KEY`
3. Configure CORS origins in `app/main.py`
4. Use environment variables for all secrets
5. Set up proper logging
6. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)

