# Changelog

## New Features Added

### Movie Ratings & Reviews System

**Database Changes:**
- Added `Review` model with:
  - `movie_id` (foreign key to Movie)
  - `user_id` (foreign key to User)
  - `rating` (1-10 scale)
  - `review_text` (optional text review)
  - Unique constraint: one review per user per movie

- Updated `Movie` model:
  - Added `tmdb_id` field for TMDB integration
  - Added `average_rating` field (automatically calculated from reviews)

**API Endpoints:**
- `POST /api/reviews` - Create a review/rating
- `GET /api/reviews/movie/{movie_id}` - Get all reviews for a movie
- `GET /api/reviews/user/{user_id}` - Get all reviews by a user
- `GET /api/reviews/me` - Get current user's reviews
- `GET /api/reviews/{review_id}` - Get a specific review
- `PUT /api/reviews/{review_id}` - Update a review (author only)
- `DELETE /api/reviews/{review_id}` - Delete a review (author only)

**Features:**
- Automatic average rating calculation when reviews are created/updated/deleted
- Users can only have one review per movie (enforced by unique constraint)
- Reviews include user information and movie details
- Rating validation (1-10 scale)

### TMDB (The Movie Database) Integration

**New Service:**
- `TMDBService` class for interacting with TMDB API
- Methods for searching, getting details, credits, popular movies, etc.
- Automatic formatting of TMDB data to match our Movie model

**API Endpoints:**
- `GET /api/tmdb/search` - Search movies on TMDB
- `GET /api/tmdb/movie/{tmdb_id}` - Get movie details from TMDB
- `POST /api/tmdb/import/{tmdb_id}` - Import a movie from TMDB into our database
- `GET /api/tmdb/popular` - Get popular movies from TMDB
- `GET /api/tmdb/top-rated` - Get top rated movies from TMDB
- `GET /api/tmdb/upcoming` - Get upcoming movies from TMDB

**Features:**
- Search millions of movies from TMDB
- Import movies with full details (cast, director, genres, poster, etc.)
- Check if movies already exist locally before importing
- TMDB ID stored for reference and future updates
- All endpoints check for existing movies and include `local_id` in responses

**Configuration:**
- Requires `TMDB_API_KEY` environment variable
- Get free API key at https://www.themoviedb.org/settings/api

## Updated Files

- `app/models.py` - Added Review model, updated Movie model
- `app/schemas.py` - Added review schemas, updated movie schemas
- `app/routers/reviews.py` - New router for review endpoints
- `app/routers/tmdb.py` - New router for TMDB integration
- `app/services/tmdb_service.py` - New TMDB API service
- `app/main.py` - Added review and TMDB routers
- `requirements.txt` - Added `requests` library
- `README.md` - Updated with new features
- `API_EXAMPLES.md` - Added examples for reviews and TMDB
- `SETUP.md` - New setup guide with TMDB configuration

## Migration Notes

When upgrading:

1. **Database Migration:**
   - The database will automatically create new tables when you restart the app
   - Existing movies will have `tmdb_id` and `average_rating` as NULL
   - You can import movies from TMDB to populate `tmdb_id`

2. **Environment Variables:**
   - Add `TMDB_API_KEY` to your `.env` file
   - Get a free API key from TMDB

3. **Dependencies:**
   - Run `pip install -r requirements.txt` to install `requests`

## Usage Examples

### Creating a Review
```python
POST /api/reviews
{
  "movie_id": 1,
  "rating": 9,
  "review_text": "Excellent movie!"
}
```

### Searching TMDB
```python
GET /api/tmdb/search?query=inception
```

### Importing from TMDB
```python
POST /api/tmdb/import/27205  # Inception TMDB ID
```

## Next Steps

Potential future enhancements:
- Review reactions/likes
- Review comments/replies
- Movie watchlists
- User follow system
- Advanced recommendation algorithms using review data
- Batch import from TMDB
- Sync movie data from TMDB periodically

