"""Movie recommendation service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models import Movie, UserPreferences, Room, User


class RecommendationService:
    """Service for generating movie recommendations."""

    @staticmethod
    def get_recommendations(
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[tuple[Movie, str]]:
        """
        Get personalized movie recommendations for a user.
        Returns list of tuples: (Movie, reason_string)
        """
        # Get user preferences
        preferences = db.query(UserPreferences).filter(
            UserPreferences.user_id == user_id
        ).first()

        recommendations = []
        
        if preferences:
            # Build query based on preferences
            query = db.query(Movie)
            
            # Filter by favorite genres if specified
            if preferences.favorite_genres:
                genres = [g.strip() for g in preferences.favorite_genres.split(",")]
                genre_filters = [
                    Movie.genre.ilike(f"%{genre}%") for genre in genres
                ]
                if genre_filters:
                    query = query.filter(or_(*genre_filters))
            
            # Filter by favorite directors if specified
            if preferences.favorite_directors:
                directors = [d.strip() for d in preferences.favorite_directors.split(",")]
                director_filters = [
                    Movie.director.ilike(f"%{director}%") for director in directors
                ]
                if director_filters:
                    query = query.filter(or_(*director_filters))
            
            # Filter by favorite actors if specified
            if preferences.favorite_actors:
                actors = [a.strip() for a in preferences.favorite_actors.split(",")]
                actor_filters = [
                    Movie.cast.ilike(f"%{actor}%") for actor in actors
                ]
                if actor_filters:
                    query = query.filter(or_(*actor_filters))
            
            # Filter by minimum rating if specified
            # Note: We'll filter by rating in the scoring phase since imdb_rating is stored as string
            
            # Get movies user hasn't joined rooms for
            user_room_movie_ids = db.query(Room.movie_id).join(
                Room.members
            ).filter(
                User.id == user_id
            ).distinct().all()
            user_room_movie_ids = [r[0] for r in user_room_movie_ids]
            
            if user_room_movie_ids:
                query = query.filter(~Movie.id.in_(user_room_movie_ids))
            
            movies = query.limit(limit * 2).all()  # Get more to filter
            
            # Score and rank movies
            scored_movies = []
            for movie in movies:
                score = 0
                reasons = []
                
                if preferences.favorite_genres and movie.genre:
                    for genre in genres:
                        if genre.lower() in movie.genre.lower():
                            score += 3
                            reasons.append(f"Matches your favorite genre: {genre}")
                            break
                
                if preferences.favorite_directors and movie.director:
                    for director in directors:
                        if director.lower() in movie.director.lower():
                            score += 5
                            reasons.append(f"Directed by {director}")
                            break
                
                if preferences.favorite_actors and movie.cast:
                    for actor in actors:
                        if actor.lower() in movie.cast.lower():
                            score += 4
                            reasons.append(f"Features {actor}")
                            break
                
                if movie.imdb_rating:
                    try:
                        rating = float(movie.imdb_rating)
                        # Check if meets minimum rating preference
                        if preferences.min_rating and rating < preferences.min_rating:
                            continue  # Skip movies below minimum rating
                        if rating >= 7.0:
                            score += 2
                            reasons.append(f"Highly rated ({movie.imdb_rating}/10)")
                    except (ValueError, TypeError):
                        pass
                
                if score > 0:
                    reason = "; ".join(reasons[:2]) if reasons else "Based on your preferences"
                    scored_movies.append((movie, score, reason))
            
            # Sort by score and return top results
            scored_movies.sort(key=lambda x: x[1], reverse=True)
            recommendations = [(movie, reason) for movie, score, reason in scored_movies[:limit]]
        
        # If no preferences or not enough recommendations, add popular movies
        if len(recommendations) < limit:
            # Get popular movies (highly rated, not in user's rooms)
            user_room_movie_ids = db.query(Room.movie_id).join(
                Room.members
            ).filter(
                User.id == user_id
            ).distinct().all()
            user_room_movie_ids = [r[0] for r in user_room_movie_ids]
            
            popular_query = db.query(Movie).filter(
                Movie.imdb_rating.isnot(None)
            )
            
            if user_room_movie_ids:
                popular_query = popular_query.filter(~Movie.id.in_(user_room_movie_ids))
            
            popular_movies = popular_query.order_by(
                Movie.imdb_rating.desc()
            ).limit(limit - len(recommendations)).all()
            
            for movie in popular_movies:
                reason = f"Highly rated ({movie.imdb_rating}/10)" if movie.imdb_rating else "Popular choice"
                recommendations.append((movie, reason))
        
        return recommendations[:limit]

    @staticmethod
    def get_similar_movies(
        db: Session,
        movie_id: int,
        limit: int = 5
    ) -> List[Movie]:
        """Get movies similar to a given movie."""
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return []
        
        query = db.query(Movie).filter(Movie.id != movie_id)
        
        # Find movies with similar genres
        if movie.genre:
            genres = [g.strip() for g in movie.genre.split(",")]
            genre_filters = [
                Movie.genre.ilike(f"%{genre}%") for genre in genres
            ]
            if genre_filters:
                query = query.filter(or_(*genre_filters))
        
        # Find movies by same director
        if movie.director:
            query = query.filter(Movie.director.ilike(f"%{movie.director}%"))
        
        return query.limit(limit).all()

