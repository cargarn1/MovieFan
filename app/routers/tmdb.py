"""TMDB integration routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie
from app.schemas import MovieResponse, MovieCreate
from app.auth import get_current_user
from app.services.tmdb_service import TMDBService

router = APIRouter(prefix="/api/tmdb", tags=["tmdb"])


@router.get("/search")
def search_tmdb_movies(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Search for movies on TMDB."""
    try:
        result = TMDBService.search_movies(query, page)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TMDB API unavailable. Please check your API key."
            )
        
        # Check which movies already exist in our database
        tmdb_ids = [movie.get("id") for movie in result.get("results", [])]
        existing_movies = {
            m.tmdb_id: m.id
            for m in db.query(Movie).filter(Movie.tmdb_id.in_(tmdb_ids)).all()
        }
        
        # Add local_id to each result if movie exists
        for movie in result.get("results", []):
            tmdb_id = movie.get("id")
            if tmdb_id in existing_movies:
                movie["local_id"] = existing_movies[tmdb_id]
            else:
                movie["local_id"] = None
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/movie/{tmdb_id}")
def get_tmdb_movie_details(tmdb_id: int, db: Session = Depends(get_db)):
    """Get detailed movie information from TMDB."""
    try:
        movie_data = TMDBService.get_movie_details(tmdb_id)
        if not movie_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found on TMDB"
            )
        
        credits_data = TMDBService.get_movie_credits(tmdb_id)
        formatted_data = TMDBService.format_movie_data(movie_data, credits_data)
        
        # Check if movie already exists in our database
        existing_movie = db.query(Movie).filter(
            Movie.tmdb_id == tmdb_id
        ).first()
        
        if existing_movie:
            formatted_data["local_id"] = existing_movie.id
            formatted_data["exists_locally"] = True
        else:
            formatted_data["exists_locally"] = False
        
        return formatted_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/import/{tmdb_id}", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def import_movie_from_tmdb(
    tmdb_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import a movie from TMDB into our database."""
    # Check if movie already exists
    existing_movie = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
    if existing_movie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Movie already exists with ID: {existing_movie.id}"
        )
    
    try:
        # Import movie data from TMDB
        formatted_data = TMDBService.import_movie_from_tmdb(tmdb_id)
        
        if not formatted_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found on TMDB"
            )
        
        # Create movie in our database
        movie = Movie(**formatted_data)
        db.add(movie)
        db.commit()
        db.refresh(movie)
        
        return movie
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/popular")
def get_popular_movies(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Get popular movies from TMDB."""
    try:
        result = TMDBService.get_popular_movies(page)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TMDB API unavailable"
            )
        
        # Check which movies already exist
        tmdb_ids = [movie.get("id") for movie in result.get("results", [])]
        existing_movies = {
            m.tmdb_id: m.id
            for m in db.query(Movie).filter(Movie.tmdb_id.in_(tmdb_ids)).all()
        }
        
        for movie in result.get("results", []):
            tmdb_id = movie.get("id")
            if tmdb_id in existing_movies:
                movie["local_id"] = existing_movies[tmdb_id]
            else:
                movie["local_id"] = None
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/top-rated")
def get_top_rated_movies(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Get top rated movies from TMDB."""
    try:
        result = TMDBService.get_top_rated_movies(page)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TMDB API unavailable"
            )
        
        # Check which movies already exist
        tmdb_ids = [movie.get("id") for movie in result.get("results", [])]
        existing_movies = {
            m.tmdb_id: m.id
            for m in db.query(Movie).filter(Movie.tmdb_id.in_(tmdb_ids)).all()
        }
        
        for movie in result.get("results", []):
            tmdb_id = movie.get("id")
            if tmdb_id in existing_movies:
                movie["local_id"] = existing_movies[tmdb_id]
            else:
                movie["local_id"] = None
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/upcoming")
def get_upcoming_movies(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Get upcoming movies from TMDB."""
    try:
        result = TMDBService.get_upcoming_movies(page)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TMDB API unavailable"
            )
        
        # Check which movies already exist
        tmdb_ids = [movie.get("id") for movie in result.get("results", [])]
        existing_movies = {
            m.tmdb_id: m.id
            for m in db.query(Movie).filter(Movie.tmdb_id.in_(tmdb_ids)).all()
        }
        
        for movie in result.get("results", []):
            tmdb_id = movie.get("id")
            if tmdb_id in existing_movies:
                movie["local_id"] = existing_movies[tmdb_id]
            else:
                movie["local_id"] = None
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

