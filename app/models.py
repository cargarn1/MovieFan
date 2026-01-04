"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Association table for many-to-many relationship between users and rooms
room_members = Table(
    'room_members',
    Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_admin', Boolean, default=False)
)


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    api_key = Column(String(255), nullable=True, unique=True, index=True)  # For Zapier integration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    rooms_created = relationship("Room", back_populates="creator", foreign_keys="Room.creator_id")
    room_memberships = relationship("Room", secondary=room_members, back_populates="members")
    invitations_sent = relationship("Invitation", back_populates="inviter", foreign_keys="Invitation.inviter_id")
    invitations_received = relationship("Invitation", back_populates="invitee", foreign_keys="Invitation.invitee_id")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    webhook_subscriptions = relationship("WebhookSubscription", back_populates="user", cascade="all, delete-orphan")


class UserPreferences(Base):
    """User movie preferences for recommendations."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Preference fields (comma-separated genres, or JSON)
    favorite_genres = Column(String(500), nullable=True)  # e.g., "Action,Comedy,Drama"
    favorite_directors = Column(String(500), nullable=True)
    favorite_actors = Column(String(500), nullable=True)
    min_rating = Column(Integer, default=0)  # Minimum rating preference (0-10)
    preferred_decades = Column(String(100), nullable=True)  # e.g., "1990s,2000s,2010s"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")


class Movie(Base):
    """Movie model."""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    year = Column(Integer, nullable=True)
    genre = Column(String(200), nullable=True)  # Comma-separated genres
    director = Column(String(200), nullable=True)
    cast = Column(String(500), nullable=True)  # Comma-separated actors
    plot = Column(Text, nullable=True)
    rating = Column(String(10), nullable=True)  # e.g., "PG-13", "R"
    imdb_rating = Column(String(10), nullable=True)  # e.g., "8.5"
    poster_url = Column(String(500), nullable=True)
    trailer_url = Column(String(500), nullable=True)
    tmdb_id = Column(Integer, nullable=True, index=True)  # The Movie Database ID
    average_rating = Column(String(10), nullable=True)  # Average user rating (calculated)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    rooms = relationship("Room", back_populates="movie")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")


class Room(Base):
    """Room model for movie discussions."""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_private = Column(Boolean, default=False)
    max_members = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    movie = relationship("Movie", back_populates="rooms")
    creator = relationship("User", back_populates="rooms_created", foreign_keys=[creator_id])
    members = relationship("User", secondary=room_members, back_populates="room_memberships")
    invitations = relationship("Invitation", back_populates="room", cascade="all, delete-orphan")


class Invitation(Base):
    """Room invitation model."""
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invitee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, declined
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    room = relationship("Room", back_populates="invitations")
    inviter = relationship("User", back_populates="invitations_sent", foreign_keys=[inviter_id])
    invitee = relationship("User", back_populates="invitations_received", foreign_keys=[invitee_id])


class Review(Base):
    """Movie review/rating model."""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-10 scale
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    # Unique constraint: one review per user per movie
    __table_args__ = (
        UniqueConstraint('movie_id', 'user_id', name='unique_user_movie_review'),
    )


class WebhookSubscription(Base):
    """Webhook subscription model for Zapier triggers."""
    __tablename__ = "webhook_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(String(50), nullable=False)  # new_room, new_review, new_movie, etc.
    webhook_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    secret = Column(String(255), nullable=True)  # Optional webhook secret for verification
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="webhook_subscriptions")
