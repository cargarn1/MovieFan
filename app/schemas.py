"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    id: int
    bio: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# User Preferences Schemas
class UserPreferencesBase(BaseModel):
    favorite_genres: Optional[str] = None
    favorite_directors: Optional[str] = None
    favorite_actors: Optional[str] = None
    min_rating: Optional[int] = Field(None, ge=0, le=10)
    preferred_decades: Optional[str] = None


class UserPreferencesResponse(UserPreferencesBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Movie Schemas
class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    plot: Optional[str] = None
    rating: Optional[str] = None
    imdb_rating: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    tmdb_id: Optional[int] = None


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int
    average_rating: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Room Schemas
class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    movie_id: int
    is_private: bool = False
    max_members: int = Field(default=50, ge=2, le=200)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_private: Optional[bool] = None
    max_members: Optional[int] = Field(None, ge=2, le=200)


class RoomResponse(RoomBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    movie: Optional[MovieResponse] = None
    creator: Optional[UserResponse] = None
    member_count: Optional[int] = None

    class Config:
        from_attributes = True


class RoomDetailResponse(RoomResponse):
    members: List[UserResponse] = []

    class Config:
        from_attributes = True


# Invitation Schemas
class InvitationBase(BaseModel):
    invitee_id: int
    message: Optional[str] = None


class InvitationCreate(InvitationBase):
    room_id: int


class InvitationResponse(BaseModel):
    id: int
    room_id: int
    inviter_id: int
    invitee_id: int
    status: str
    message: Optional[str] = None
    created_at: datetime
    room: Optional[RoomResponse] = None
    inviter: Optional[UserResponse] = None
    invitee: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Recommendation Schema
class RecommendationResponse(BaseModel):
    movie: MovieResponse
    reason: str  # Why this movie was recommended


# Review Schemas
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    movie_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=10)
    review_text: Optional[str] = None


class ReviewResponse(ReviewBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[UserResponse] = None
    movie: Optional[MovieResponse] = None

    class Config:
        from_attributes = True

