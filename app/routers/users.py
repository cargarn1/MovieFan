"""User management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserPreferences
from app.schemas import UserResponse, UserUpdate, UserPreferencesBase, UserPreferencesResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/preferences", response_model=UserPreferencesResponse)
def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()
    
    if not preferences:
        # Create default preferences if they don't exist
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    
    return preferences


@router.put("/me/preferences", response_model=UserPreferencesResponse)
def update_user_preferences(
    preferences_data: UserPreferencesBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()
    
    if not preferences:
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)
    
    if preferences_data.favorite_genres is not None:
        preferences.favorite_genres = preferences_data.favorite_genres
    if preferences_data.favorite_directors is not None:
        preferences.favorite_directors = preferences_data.favorite_directors
    if preferences_data.favorite_actors is not None:
        preferences.favorite_actors = preferences_data.favorite_actors
    if preferences_data.min_rating is not None:
        preferences.min_rating = preferences_data.min_rating
    if preferences_data.preferred_decades is not None:
        preferences.preferred_decades = preferences_data.preferred_decades
    
    db.commit()
    db.refresh(preferences)
    return preferences


@router.get("/me/api-key", response_model=dict)
def get_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get or create API key for current user (for Zapier integration)."""
    from app.auth import generate_api_key
    
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

