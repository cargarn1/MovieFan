"""Zapier integration routes - webhooks and Zapier-friendly endpoints."""
import requests
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import User, Room, Review, Movie, WebhookSubscription
from app.schemas import RoomResponse, ReviewResponse, MovieResponse
from app.auth import get_current_user_or_api_key, generate_api_key

router = APIRouter(prefix="/api/zapier", tags=["zapier"])


def trigger_webhook(webhook_url: str, payload: dict, secret: Optional[str] = None):
    """Trigger a webhook with the given payload."""
    try:
        headers = {"Content-Type": "application/json"}
        if secret:
            headers["X-Webhook-Secret"] = secret
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Webhook error: {e}")
        return False


def notify_webhooks(
    db: Session,
    event_type: str,
    payload: dict,
    user_id: Optional[int] = None
):
    """Notify all active webhooks for a given event type."""
    query = db.query(WebhookSubscription).filter(
        WebhookSubscription.event_type == event_type,
        WebhookSubscription.is_active == True
    )
    
    if user_id:
        query = query.filter(WebhookSubscription.user_id == user_id)
    
    subscriptions = query.all()
    
    for subscription in subscriptions:
        trigger_webhook(
            subscription.webhook_url,
            payload,
            subscription.secret
        )


@router.get("/api-key", response_model=dict)
def get_or_create_api_key(
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """Get or create an API key for Zapier integration."""
    if current_user.api_key:
        return {
            "api_key": current_user.api_key,
            "message": "Use this API key in Zapier: X-API-Key header"
        }
    
    # Generate new API key
    api_key = generate_api_key()
    current_user.api_key = api_key
    db.commit()
    
    return {
        "api_key": api_key,
        "message": "New API key generated. Use this in Zapier: X-API-Key header"
    }


@router.post("/webhooks", status_code=status.HTTP_201_CREATED)
def create_webhook_subscription(
    event_type: str,
    webhook_url: str,
    secret: Optional[str] = None,
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """Create a webhook subscription for Zapier triggers."""
    valid_event_types = ["new_room", "new_review", "new_movie", "room_joined"]
    
    if event_type not in valid_event_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid event_type. Must be one of: {', '.join(valid_event_types)}"
        )
    
    subscription = WebhookSubscription(
        user_id=current_user.id,
        event_type=event_type,
        webhook_url=webhook_url,
        secret=secret,
        is_active=True
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return {
        "id": subscription.id,
        "event_type": subscription.event_type,
        "webhook_url": subscription.webhook_url,
        "is_active": subscription.is_active,
        "message": "Webhook subscription created"
    }


@router.get("/webhooks", response_model=List[dict])
def list_webhook_subscriptions(
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """List all webhook subscriptions for the current user."""
    subscriptions = db.query(WebhookSubscription).filter(
        WebhookSubscription.user_id == current_user.id
    ).all()
    
    return [
        {
            "id": sub.id,
            "event_type": sub.event_type,
            "webhook_url": sub.webhook_url,
            "is_active": sub.is_active,
            "created_at": sub.created_at.isoformat()
        }
        for sub in subscriptions
    ]


@router.delete("/webhooks/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """Delete a webhook subscription."""
    subscription = db.query(WebhookSubscription).filter(
        WebhookSubscription.id == subscription_id,
        WebhookSubscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook subscription not found"
        )
    
    db.delete(subscription)
    db.commit()


# Zapier-friendly action endpoints
@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room_zapier(
    name: str,
    movie_id: int,
    description: Optional[str] = None,
    is_private: bool = False,
    max_members: int = 50,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """Create a room (Zapier-friendly endpoint)."""
    from app.models import Movie as MovieModel
    from app.services.room_service import RoomService
    
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    room = RoomService.create_room(
        db=db,
        creator_id=current_user.id,
        name=name,
        movie_id=movie_id,
        description=description,
        is_private=is_private,
        max_members=max_members
    )
    
    room.member_count = len(room.members)
    
    # Trigger webhook
    background_tasks.add_task(
        notify_webhooks,
        db,
        "new_room",
        {
            "event": "new_room",
            "room_id": room.id,
            "room_name": room.name,
            "movie_id": room.movie_id,
            "movie_title": movie.title,
            "creator_id": room.creator_id,
            "created_at": room.created_at.isoformat()
        }
    )
    
    return room


@router.post("/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review_zapier(
    movie_id: int,
    rating: int,
    review_text: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """Create a review (Zapier-friendly endpoint)."""
    from app.schemas import ReviewCreate
    from app.routers.reviews import update_movie_average_rating
    
    # Verify movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # Check if user already reviewed this movie
    existing_review = db.query(Review).filter(
        Review.movie_id == movie_id,
        Review.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this movie. Use update endpoint to modify your review."
        )
    
    # Create review
    review = Review(
        movie_id=movie_id,
        user_id=current_user.id,
        rating=rating,
        review_text=review_text
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update movie's average rating
    update_movie_average_rating(db, movie_id)
    
    # Trigger webhook
    background_tasks.add_task(
        notify_webhooks,
        db,
        "new_review",
        {
            "event": "new_review",
            "review_id": review.id,
            "movie_id": review.movie_id,
            "movie_title": movie.title if movie else None,
            "rating": review.rating,
            "user_id": review.user_id,
            "created_at": review.created_at.isoformat()
        }
    )
    
    return review


@router.get("/rooms", response_model=List[RoomResponse])
def list_rooms_zapier(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    movie_id: Optional[int] = None,
    current_user: Optional[User] = Depends(get_current_user_or_api_key),
    db: Session = Depends(get_db)
):
    """List rooms (Zapier-friendly endpoint)."""
    query = db.query(Room)
    
    if movie_id:
        query = query.filter(Room.movie_id == movie_id)
    
    rooms = query.order_by(desc(Room.created_at)).offset(skip).limit(limit).all()
    
    for room in rooms:
        room.member_count = len(room.members)
    
    return rooms


@router.get("/reviews", response_model=List[ReviewResponse])
def list_reviews_zapier(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    movie_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List reviews (Zapier-friendly endpoint)."""
    query = db.query(Review)
    
    if movie_id:
        query = query.filter(Review.movie_id == movie_id)
    
    reviews = query.order_by(desc(Review.created_at)).offset(skip).limit(limit).all()
    return reviews


@router.get("/movies", response_model=List[MovieResponse])
def list_movies_zapier(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List movies (Zapier-friendly endpoint)."""
    from sqlalchemy import or_
    
    query = db.query(Movie)
    
    if search:
        query = query.filter(
            or_(
                Movie.title.ilike(f"%{search}%"),
                Movie.plot.ilike(f"%{search}%")
            )
        )
    
    movies = query.order_by(desc(Movie.created_at)).offset(skip).limit(limit).all()
    return movies


@router.get("/test", response_model=dict)
def test_connection(
    current_user: User = Depends(get_current_user_or_api_key)
):
    """Test connection endpoint for Zapier."""
    return {
        "status": "success",
        "message": "Connection successful",
        "user_id": current_user.id,
        "username": current_user.username
    }

