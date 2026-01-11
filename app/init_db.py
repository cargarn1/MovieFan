"""Initialize database with sample data."""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Movie, UserPreferences
from app.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

# Sample movies data
SAMPLE_MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama",
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "rating": "R",
        "imdb_rating": "9.3",
        "poster_url": "https://example.com/posters/shawshank.jpg"
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genre": "Crime, Drama",
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "rating": "R",
        "imdb_rating": "9.2",
        "poster_url": "https://example.com/posters/godfather.jpg"
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action, Crime, Drama",
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "rating": "PG-13",
        "imdb_rating": "9.0",
        "poster_url": "https://example.com/posters/darkknight.jpg"
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "genre": "Crime, Drama",
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "rating": "R",
        "imdb_rating": "8.9",
        "poster_url": "https://example.com/posters/pulpfiction.jpg"
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Sci-Fi, Thriller",
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Marion Cotillard, Tom Hardy",
        "plot": "A skilled thief is given a chance at redemption if he can accomplish the impossible task of inception.",
        "rating": "PG-13",
        "imdb_rating": "8.8",
        "poster_url": "https://example.com/posters/inception.jpg"
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genre": "Action, Sci-Fi",
        "director": "Lana Wachowski, Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "plot": "A computer hacker learns about the true nature of reality and his role in the war against its controllers.",
        "rating": "R",
        "imdb_rating": "8.7",
        "poster_url": "https://example.com/posters/matrix.jpg"
    },
    {
        "title": "Goodfellas",
        "year": 1990,
        "genre": "Biography, Crime, Drama",
        "director": "Martin Scorsese",
        "cast": "Robert De Niro, Ray Liotta, Joe Pesci",
        "plot": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.",
        "rating": "R",
        "imdb_rating": "8.7",
        "poster_url": "https://example.com/posters/goodfellas.jpg"
    },
    {
        "title": "Fight Club",
        "year": 1999,
        "genre": "Drama",
        "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter",
        "plot": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much bigger.",
        "rating": "R",
        "imdb_rating": "8.8",
        "poster_url": "https://example.com/posters/fightclub.jpg"
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama, Romance",
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "plot": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.",
        "rating": "PG-13",
        "imdb_rating": "8.8",
        "poster_url": "https://example.com/posters/forrestgump.jpg"
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "year": 2003,
        "genre": "Action, Adventure, Drama",
        "director": "Peter Jackson",
        "cast": "Elijah Wood, Viggo Mortensen, Ian McKellen",
        "plot": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
        "rating": "PG-13",
        "imdb_rating": "8.9",
        "poster_url": "https://example.com/posters/lotr.jpg"
    }
]


def init_db():
    """Initialize database with sample data."""
    db: Session = SessionLocal()
    
    try:
        # Check if movies already exist
        existing_movies = db.query(Movie).count()
        if existing_movies > 0:
            print(f"Database already has {existing_movies} movies. Skipping initialization.")
            return
        
        # Add sample movies
        print("Adding sample movies...")
        for movie_data in SAMPLE_MOVIES:
            movie = Movie(**movie_data)
            db.add(movie)
        
        db.commit()
        print(f"Successfully added {len(SAMPLE_MOVIES)} movies to the database.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")



