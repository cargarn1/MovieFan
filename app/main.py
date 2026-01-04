"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, movies, rooms, reviews, tmdb, zapier

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="MovieFan API",
    description="Movie Recommendation & Social Platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(rooms.router)
app.include_router(reviews.router)
app.include_router(tmdb.router)
app.include_router(zapier.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to MovieFan API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

