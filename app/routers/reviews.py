"""Review/rating routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Review, Movie, User
from app.schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


def update_movie_average_rating(db: Session, movie_id: int):
    """Update movie's average rating based on all reviews."""
    avg_result = db.query(func.avg(Review.rating)).filter(
        Review.movie_id == movie_id
    ).scalar()
    
    if avg_result:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            movie.average_rating = f"{avg_result:.2f}"
            db.commit()


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new review/rating for a movie."""
    # Verify movie exists
    movie = db.query(Movie).filter(Movie.id == review_data.movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # Check if user already reviewed this movie
    existing_review = db.query(Review).filter(
        Review.movie_id == review_data.movie_id,
        Review.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this movie. Use update endpoint to modify your review."
        )
    
    # Create review
    review = Review(
        movie_id=review_data.movie_id,
        user_id=current_user.id,
        rating=review_data.rating,
        review_text=review_data.review_text
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update movie's average rating
    update_movie_average_rating(db, review_data.movie_id)
    
    return review


@router.get("/movie/{movie_id}", response_model=list[ReviewResponse])
def get_movie_reviews(
    movie_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all reviews for a specific movie."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    reviews = db.query(Review).filter(
        Review.movie_id == movie_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.get("/user/{user_id}", response_model=list[ReviewResponse])
def get_user_reviews(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all reviews by a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    reviews = db.query(Review).filter(
        Review.user_id == user_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.get("/me", response_model=list[ReviewResponse])
def get_my_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's reviews."""
    reviews = db.query(Review).filter(
        Review.user_id == current_user.id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a review (only the author can update)."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.review_text is not None:
        review.review_text = review_update.review_text
    
    db.commit()
    db.refresh(review)
    
    # Update movie's average rating
    update_movie_average_rating(db, review.movie_id)
    
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a review (only the author can delete)."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    movie_id = review.movie_id
    db.delete(review)
    db.commit()
    
    # Update movie's average rating
    update_movie_average_rating(db, movie_id)



