"""TMDB (The Movie Database) API service."""
import requests
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


class TMDBService:
    """Service for interacting with The Movie Database API."""

    @staticmethod
    def _make_request(endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a request to TMDB API."""
        if not TMDB_API_KEY:
            raise ValueError("TMDB_API_KEY not set in environment variables")
        
        url = f"{TMDB_BASE_URL}{endpoint}"
        params = params or {}
        params["api_key"] = TMDB_API_KEY
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"TMDB API error: {e}")
            return None

    @staticmethod
    def search_movies(query: str, page: int = 1) -> Optional[Dict]:
        """Search for movies by title."""
        return TMDBService._make_request(
            "/search/movie",
            params={"query": query, "page": page}
        )

    @staticmethod
    def get_movie_details(tmdb_id: int) -> Optional[Dict]:
        """Get detailed information about a movie."""
        return TMDBService._make_request(f"/movie/{tmdb_id}")

    @staticmethod
    def get_movie_credits(tmdb_id: int) -> Optional[Dict]:
        """Get cast and crew information for a movie."""
        return TMDBService._make_request(f"/movie/{tmdb_id}/credits")

    @staticmethod
    def get_popular_movies(page: int = 1) -> Optional[Dict]:
        """Get popular movies."""
        return TMDBService._make_request("/movie/popular", params={"page": page})

    @staticmethod
    def get_top_rated_movies(page: int = 1) -> Optional[Dict]:
        """Get top rated movies."""
        return TMDBService._make_request("/movie/top_rated", params={"page": page})

    @staticmethod
    def get_upcoming_movies(page: int = 1) -> Optional[Dict]:
        """Get upcoming movies."""
        return TMDBService._make_request("/movie/upcoming", params={"page": page})

    @staticmethod
    def get_now_playing_movies(page: int = 1) -> Optional[Dict]:
        """Get movies currently playing in theaters."""
        return TMDBService._make_request("/movie/now_playing", params={"page": page})

    @staticmethod
    def format_movie_data(tmdb_data: Dict, credits_data: Optional[Dict] = None) -> Dict:
        """
        Format TMDB movie data to match our Movie model.
        
        Args:
            tmdb_data: Movie data from TMDB API
            credits_data: Optional credits data for cast/director info
        
        Returns:
            Formatted movie data dictionary
        """
        # Extract genres
        genres = ", ".join([g["name"] for g in tmdb_data.get("genres", [])])
        
        # Extract director from crew
        director = None
        if credits_data:
            crew = credits_data.get("crew", [])
            directors = [p for p in crew if p.get("job") == "Director"]
            if directors:
                director = directors[0].get("name")
        
        # Extract main cast
        cast_list = []
        if credits_data:
            cast = credits_data.get("cast", [])[:10]  # Top 10 cast members
            cast_list = [actor.get("name") for actor in cast]
        
        # Format rating (TMDB uses 0-10 scale, we'll convert to string)
        vote_average = tmdb_data.get("vote_average")
        imdb_rating = f"{vote_average:.1f}" if vote_average else None
        
        # Get poster URL
        poster_path = tmdb_data.get("poster_path")
        poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
        
        return {
            "title": tmdb_data.get("title"),
            "year": int(tmdb_data.get("release_date", "").split("-")[0]) if tmdb_data.get("release_date") else None,
            "genre": genres if genres else None,
            "director": director,
            "cast": ", ".join(cast_list) if cast_list else None,
            "plot": tmdb_data.get("overview"),
            "rating": tmdb_data.get("certification") or None,  # May need to get from different endpoint
            "imdb_rating": imdb_rating,
            "poster_url": poster_url,
            "tmdb_id": tmdb_data.get("id"),
        }

    @staticmethod
    def import_movie_from_tmdb(tmdb_id: int) -> Optional[Dict]:
        """
        Import a movie from TMDB by ID.
        Returns formatted movie data ready to be saved to database.
        """
        movie_data = TMDBService.get_movie_details(tmdb_id)
        if not movie_data:
            return None
        
        credits_data = TMDBService.get_movie_credits(tmdb_id)
        formatted_data = TMDBService.format_movie_data(movie_data, credits_data)
        
        return formatted_data

