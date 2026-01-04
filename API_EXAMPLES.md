# MovieFan API - Quick Reference Guide

## Getting Started

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize database with sample movies:**
```bash
python -m app.init_db
```

3. **Run the server:**
```bash
python run.py
# or
uvicorn app.main:app --reload
```

4. **Access API docs:**
Open http://localhost:8001/docs in your browser

## Example API Usage

### 1. Register a New User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "movielover",
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "Movie Lover"
}
```

### 2. Login and Get Token

```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=movielover&password=securepassword123
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 3. Get Current User Info

```bash
GET /api/auth/me
Authorization: Bearer <your_token>
```

### 4. Update User Preferences

```bash
PUT /api/users/me/preferences
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "favorite_genres": "Action,Comedy,Drama",
  "favorite_directors": "Christopher Nolan,Quentin Tarantino",
  "favorite_actors": "Leonardo DiCaprio,Tom Hanks",
  "min_rating": 7,
  "preferred_decades": "1990s,2000s,2010s"
}
```

### 5. List Movies

```bash
GET /api/movies?search=matrix&limit=10
```

### 6. Get Movie Recommendations

```bash
GET /api/movies/recommendations/me?limit=10
Authorization: Bearer <your_token>
```

### 7. Create a Room

```bash
POST /api/rooms
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "name": "The Matrix Discussion",
  "description": "Let's discuss The Matrix trilogy!",
  "movie_id": 6,
  "is_private": false,
  "max_members": 50
}
```

### 8. List Available Rooms

```bash
GET /api/rooms?movie_id=6&search=matrix
Authorization: Bearer <your_token>
```

### 9. Join a Room

```bash
POST /api/rooms/{room_id}/join
Authorization: Bearer <your_token>
```

### 10. Invite User to Room

```bash
POST /api/rooms/{room_id}/invite
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "room_id": 1,
  "invitee_id": 2,
  "message": "Join us for a great discussion!"
}
```

### 11. Get My Rooms

```bash
GET /api/rooms/my-rooms
Authorization: Bearer <your_token>
```

### 12. Get My Invitations

```bash
GET /api/rooms/invitations/me
Authorization: Bearer <your_token>
```

### 13. Accept Invitation

```bash
POST /api/rooms/invitations/{invitation_id}/accept
Authorization: Bearer <your_token>
```

### 14. Create a Review/Rating

```bash
POST /api/reviews
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "movie_id": 1,
  "rating": 9,
  "review_text": "An absolute masterpiece! One of the best films ever made."
}
```

### 15. Get Reviews for a Movie

```bash
GET /api/reviews/movie/{movie_id}?skip=0&limit=20
```

### 16. Get My Reviews

```bash
GET /api/reviews/me
Authorization: Bearer <your_token>
```

### 17. Update a Review

```bash
PUT /api/reviews/{review_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "rating": 10,
  "review_text": "Changed my mind - it's perfect!"
}
```

### 18. Search Movies on TMDB

```bash
GET /api/tmdb/search?query=inception&page=1
```

### 19. Get Movie Details from TMDB

```bash
GET /api/tmdb/movie/{tmdb_id}
```

### 20. Import Movie from TMDB

```bash
POST /api/tmdb/import/{tmdb_id}
Authorization: Bearer <your_token>
```

### 21. Get Popular Movies from TMDB

```bash
GET /api/tmdb/popular?page=1
```

### 22. Get Top Rated Movies from TMDB

```bash
GET /api/tmdb/top-rated?page=1
```

## Python Example

```python
import requests

BASE_URL = "http://localhost:8001"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
})
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    data={"username": "testuser", "password": "password123"}
)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get recommendations
response = requests.get(
    f"{BASE_URL}/api/movies/recommendations/me",
    headers=headers
)
recommendations = response.json()
print(recommendations)

# Create a room
response = requests.post(
    f"{BASE_URL}/api/rooms",
    headers=headers,
    json={
        "name": "My Movie Room",
        "movie_id": 1,
        "description": "Discussion about The Shawshank Redemption"
    }
)
room = response.json()
print(room)

# Create a review/rating
response = requests.post(
    f"{BASE_URL}/api/reviews",
    headers=headers,
    json={
        "movie_id": 1,
        "rating": 9,
        "review_text": "An absolute masterpiece! One of the best films ever made."
    }
)
review = response.json()
print(review)

# Get reviews for a movie
response = requests.get(f"{BASE_URL}/api/reviews/movie/1")
reviews = response.json()
print(reviews)

# Search TMDB for movies
response = requests.get(f"{BASE_URL}/api/tmdb/search?query=inception")
tmdb_results = response.json()
print(tmdb_results)

# Import a movie from TMDB
response = requests.post(
    f"{BASE_URL}/api/tmdb/import/27205",  # Inception TMDB ID
    headers=headers
)
imported_movie = response.json()
print(imported_movie)
```

