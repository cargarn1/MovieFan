"""Movie routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Movie
from app.schemas import MovieResponse, MovieCreate, RecommendationResponse
from app.auth import get_current_user
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=list[MovieResponse])
def list_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List movies with optional filtering."""
    query = db.query(Movie)
    
    if search:
        query = query.filter(
            or_(
                Movie.title.ilike(f"%{search}%"),
                Movie.plot.ilike(f"%{search}%"),
                Movie.director.ilike(f"%{search}%")
            )
        )
    
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    
    if year:
        query = query.filter(Movie.year == year)
    
    movies = query.order_by(Movie.year.desc(), Movie.title).offset(skip).limit(limit).all()
    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get movie by ID."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie


@router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_data: MovieCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new movie entry."""
    # Check if movie already exists
    existing = db.query(Movie).filter(
        Movie.title.ilike(movie_data.title)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already exists"
        )
    
    movie = Movie(**movie_data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.get("/recommendations/me", response_model=list[RecommendationResponse])
def get_my_recommendations(
    limit: int = Query(10, ge=1, le=50),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized movie recommendations for current user."""
    recommendations = RecommendationService.get_recommendations(
        db, current_user.id, limit
    )
    
    return [
        RecommendationResponse(movie=movie, reason=reason)
        for movie, reason in recommendations
    ]


@router.get("/{movie_id}/similar", response_model=list[MovieResponse])
def get_similar_movies(
    movie_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get movies similar to the given movie."""
    similar = RecommendationService.get_similar_movies(db, movie_id, limit)
    return similar


