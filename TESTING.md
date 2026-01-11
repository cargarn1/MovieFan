# MovieFan Testing Guide

This guide covers multiple ways to test MovieFan, from quick smoke tests to comprehensive feature testing.

## Prerequisites

1. **Backend dependencies installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Frontend dependencies installed:**
   ```bash
   cd frontend
   npm install
   ```

3. **Database initialized:**
   ```bash
   python -m app.init_db
   ```

4. **Environment variables configured:**
   - `.env` file exists with `TMDB_API_KEY` set (you just added this!)
   - `DATABASE_URL` configured
   - `SECRET_KEY` set

## Quick Start Testing

### 1. Start the Servers

**Terminal 1 - Backend API:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan
python run.py
```

Expected output: Server running on `http://0.0.0.0:5001`

**Terminal 2 - Frontend:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/frontend
npm run dev
```

Expected output: Frontend running on `http://localhost:5000`

### 2. Verify Servers Are Running

**Backend Health Check:**
```bash
curl http://localhost:5001/docs
```

**Frontend Health Check:**
```bash
curl http://localhost:5000
```

## Testing Methods

### Method 1: Interactive API Documentation (Easiest)

1. **Open Swagger UI:**
   - Navigate to: `http://localhost:5001/docs`
   - This provides an interactive interface to test all API endpoints

2. **Test Authentication:**
   - Click on `POST /api/auth/register`
   - Click "Try it out"
   - Enter test user data:
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpass123",
       "full_name": "Test User"
     }
     ```
   - Click "Execute"
   - Copy the `access_token` from the response

3. **Authorize:**
   - Click the "Authorize" button at the top
   - Enter: `Bearer <your_access_token>`
   - Now you can test protected endpoints

4. **Test Endpoints:**
   - Try creating a movie room
   - Search TMDB for movies
   - Import a movie from TMDB
   - Create a review

### Method 2: Using cURL Commands

#### Authentication Flow

```bash
# 1. Register a new user
curl -X POST "http://localhost:5001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "movielover",
    "email": "movie@example.com",
    "password": "password123",
    "full_name": "Movie Lover"
  }'

# 2. Login and get token
TOKEN=$(curl -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=movielover&password=password123" \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# 3. Get current user info
curl -X GET "http://localhost:5001/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

#### TMDB Integration Testing

```bash
# Search TMDB for movies
curl "http://localhost:5001/api/tmdb/search?query=inception"

# Get popular movies from TMDB
curl "http://localhost:5001/api/tmdb/popular?page=1"

# Get top-rated movies
curl "http://localhost:5001/api/tmdb/top-rated?page=1"

# Get movie details from TMDB (Inception has TMDB ID 27205)
curl "http://localhost:5001/api/tmdb/movie/27205"

# Import a movie from TMDB (requires authentication)
curl -X POST "http://localhost:5001/api/tmdb/import/27205" \
  -H "Authorization: Bearer $TOKEN"
```

#### Movie Management Testing

```bash
# List all movies
curl "http://localhost:5001/api/movies"

# Search movies
curl "http://localhost:5001/api/movies?search=matrix"

# Get movie details
curl "http://localhost:5001/api/movies/1"

# Get recommendations (requires authentication)
curl "http://localhost:5001/api/movies/recommendations/me" \
  -H "Authorization: Bearer $TOKEN"
```

#### Room Management Testing

```bash
# Create a room
curl -X POST "http://localhost:5001/api/rooms" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inception Discussion",
    "description": "Let'\''s discuss Inception!",
    "movie_id": 1,
    "is_private": false
  }'

# List rooms
curl "http://localhost:5001/api/rooms" \
  -H "Authorization: Bearer $TOKEN"

# Get my rooms
curl "http://localhost:5001/api/rooms/my-rooms" \
  -H "Authorization: Bearer $TOKEN"

# Join a room (replace {room_id} with actual ID)
curl -X POST "http://localhost:5001/api/rooms/1/join" \
  -H "Authorization: Bearer $TOKEN"
```

#### Review & Rating Testing

```bash
# Create a review
curl -X POST "http://localhost:5001/api/reviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "rating": 9,
    "review_text": "Amazing movie! One of my favorites."
  }'

# Get reviews for a movie
curl "http://localhost:5001/api/reviews/movie/1"

# Get my reviews
curl "http://localhost:5001/api/reviews/me" \
  -H "Authorization: Bearer $TOKEN"

# Update a review (replace {review_id} with actual ID)
curl -X PUT "http://localhost:5001/api/reviews/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 10,
    "review_text": "Changed my mind - it'\''s perfect!"
  }'
```

#### User Preferences Testing

```bash
# Update preferences
curl -X PUT "http://localhost:5001/api/users/me/preferences" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "favorite_genres": "Action,Sci-Fi,Drama",
    "favorite_directors": "Christopher Nolan",
    "favorite_actors": "Leonardo DiCaprio",
    "min_rating": 7,
    "preferred_decades": "2000s,2010s"
  }'

# Get preferences
curl "http://localhost:5001/api/users/me/preferences" \
  -H "Authorization: Bearer $TOKEN"
```

### Method 3: Using Python Scripts

Create a test script `test_moviefan.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5001"

def test_api():
    print("=" * 50)
    print("MovieFan API Testing")
    print("=" * 50)
    
    # 1. Register
    print("\n1. Registering user...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ User registered successfully")
    else:
        print(f"✗ Error: {response.text}")
        return
    
    # 2. Login
    print("\n2. Logging in...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✓ Logged in, token received")
    
    # 3. Get user info
    print("\n3. Getting user info...")
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"✓ User: {response.json()}")
    
    # 4. Search TMDB
    print("\n4. Searching TMDB for 'Inception'...")
    response = requests.get(f"{BASE_URL}/api/tmdb/search?query=inception")
    if response.status_code == 200:
        results = response.json()
        print(f"✓ Found {len(results.get('results', []))} results")
        if results.get('results'):
            print(f"  First result: {results['results'][0]['title']}")
    
    # 5. Import movie from TMDB
    print("\n5. Importing Inception from TMDB...")
    response = requests.post(
        f"{BASE_URL}/api/tmdb/import/27205",  # Inception TMDB ID
        headers=headers
    )
    if response.status_code == 201:
        movie = response.json()
        print(f"✓ Movie imported: {movie.get('title')}")
        movie_id = movie.get('id')
    else:
        print(f"✗ Error: {response.text}")
        movie_id = 1  # Use existing movie
    
    # 6. Create review
    print("\n6. Creating review...")
    response = requests.post(
        f"{BASE_URL}/api/reviews",
        headers=headers,
        json={
            "movie_id": movie_id,
            "rating": 9,
            "review_text": "Amazing movie! One of my favorites."
        }
    )
    if response.status_code == 201:
        print(f"✓ Review created: {response.json()}")
    
    # 7. Create room
    print("\n7. Creating room...")
    response = requests.post(
        f"{BASE_URL}/api/rooms",
        headers=headers,
        json={
            "name": "Inception Discussion",
            "description": "Let's discuss Inception!",
            "movie_id": movie_id,
            "is_private": False
        }
    )
    if response.status_code == 201:
        print(f"✓ Room created: {response.json()}")
    
    # 8. Get recommendations
    print("\n8. Getting recommendations...")
    response = requests.get(
        f"{BASE_URL}/api/movies/recommendations/me",
        headers=headers
    )
    if response.status_code == 200:
        recommendations = response.json()
        print(f"✓ Got {len(recommendations)} recommendations")
    
    print("\n" + "=" * 50)
    print("Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
```

Run it:
```bash
python test_moviefan.py
```

### Method 4: Frontend Testing

1. **Open the frontend:**
   - Navigate to: `http://localhost:5000`

2. **Test User Flow:**
   - Register a new account
   - Login
   - Browse movies
   - Search TMDB for movies
   - Import a movie from TMDB
   - Create a review/rating
   - Create a movie room
   - Join a room
   - Update preferences
   - View recommendations

3. **Test Features:**
   - **Authentication:** Register, login, logout
   - **Movies:** Browse, search, view details
   - **TMDB:** Search, import movies
   - **Reviews:** Create, edit, delete reviews
   - **Rooms:** Create, join, leave rooms
   - **Recommendations:** View personalized recommendations

## Comprehensive Test Checklist

### Authentication ✅
- [ ] Register new user
- [ ] Login with credentials
- [ ] Get current user info
- [ ] Logout (frontend)

### TMDB Integration ✅
- [ ] Search movies on TMDB
- [ ] Get popular movies
- [ ] Get top-rated movies
- [ ] Get upcoming movies
- [ ] Get movie details from TMDB
- [ ] Import movie from TMDB

### Movies ✅
- [ ] List all movies
- [ ] Search movies
- [ ] Get movie details
- [ ] Get similar movies
- [ ] Get recommendations

### Reviews & Ratings ✅
- [ ] Create a review
- [ ] Get reviews for a movie
- [ ] Get my reviews
- [ ] Update a review
- [ ] Delete a review
- [ ] Verify average rating updates

### Rooms ✅
- [ ] Create a room
- [ ] List rooms
- [ ] Get room details
- [ ] Join a room
- [ ] Leave a room
- [ ] Get my rooms
- [ ] Invite user to room

### User Preferences ✅
- [ ] Update preferences
- [ ] Get preferences
- [ ] Verify recommendations reflect preferences

### Zapier Integration ✅
- [ ] Get API key
- [ ] Test API connection
- [ ] Create webhook subscription
- [ ] List webhooks
- [ ] Delete webhook

## Troubleshooting

### Backend won't start
- Check if port 5001 is available: `lsof -i :5001`
- Verify `.env` file exists and has required variables
- Check database file exists: `ls -la moviefan.db`

### Frontend won't start
- Check if port 5000 is available: `lsof -i :5000`
- Verify `node_modules` installed: `cd frontend && npm install`
- Check for errors in browser console

### TMDB API errors
- Verify `TMDB_API_KEY` is set in `.env`
- Check API key is valid at https://www.themoviedb.org/settings/api
- Restart backend after updating `.env`

### Authentication errors
- Verify token is included in headers: `Authorization: Bearer <token>`
- Check token hasn't expired (default: 30 minutes)
- Re-login to get new token

### Database errors
- Reinitialize database: `python -m app.init_db`
- Check database file permissions
- Verify SQLite is working: `sqlite3 moviefan.db ".tables"`

## Quick Test Commands

```bash
# Test backend is running
curl http://localhost:5001/docs

# Test frontend is running
curl http://localhost:5000

# Quick API test (no auth required)
curl "http://localhost:5001/api/tmdb/search?query=matrix"

# Test with authentication
TOKEN=$(curl -s -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123" | jq -r '.access_token')

curl "http://localhost:5001/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## Next Steps

After basic testing:
1. Test error handling (invalid inputs, missing data)
2. Test edge cases (empty results, large datasets)
3. Test performance (multiple concurrent requests)
4. Test Zapier integration end-to-end
5. Write automated tests (pytest for backend, Jest for frontend)
