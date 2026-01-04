import { Link } from 'react-router-dom';
import { Film, Users, Star, TrendingUp } from 'lucide-react';
import { useState, useEffect } from 'react';
import { moviesService } from '../services/movies';
import { authService } from '../services/auth';

export default function Home() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const isAuthenticated = authService.isAuthenticated();

  useEffect(() => {
    const loadMovies = async () => {
      try {
        const data = await moviesService.list({ limit: 6 });
        setMovies(data);
      } catch (error) {
        console.error('Failed to load movies:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMovies();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-white sm:text-5xl md:text-6xl">
          Welcome to <span className="text-primary-400">MovieFan</span>
        </h1>
        <p className="mt-3 max-w-md mx-auto text-base text-gray-400 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          Discover movies, join discussions, and share your reviews with a community of movie lovers.
        </p>
        {!isAuthenticated && (
          <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <Link
                to="/register"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
              >
                Get started
              </Link>
            </div>
            <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
              <Link
                to="/movies"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
              >
                Browse Movies
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4 mb-12">
        <div className="bg-slate-800 rounded-lg p-6">
          <Film className="h-8 w-8 text-primary-400 mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Discover Movies</h3>
          <p className="text-gray-400 text-sm">
            Browse thousands of movies and find your next favorite film.
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6">
          <Users className="h-8 w-8 text-primary-400 mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Join Rooms</h3>
          <p className="text-gray-400 text-sm">
            Create or join discussion rooms centered around specific movies.
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6">
          <Star className="h-8 w-8 text-primary-400 mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Rate & Review</h3>
          <p className="text-gray-400 text-sm">
            Share your thoughts and ratings to help others discover great movies.
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6">
          <TrendingUp className="h-8 w-8 text-primary-400 mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Get Recommendations</h3>
          <p className="text-gray-400 text-sm">
            Receive personalized movie recommendations based on your preferences.
          </p>
        </div>
      </div>

      {/* Featured Movies */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">Featured Movies</h2>
          <Link
            to="/movies"
            className="text-primary-400 hover:text-primary-300 text-sm font-medium"
          >
            View all →
          </Link>
        </div>
        {loading ? (
          <div className="text-center text-gray-400 py-12">Loading movies...</div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {movies.map((movie) => (
              <Link
                key={movie.id}
                to={`/movies/${movie.id}`}
                className="bg-slate-800 rounded-lg overflow-hidden hover:bg-slate-700 transition-colors"
              >
                {movie.poster_url ? (
                  <img
                    src={movie.poster_url}
                    alt={movie.title}
                    className="w-full h-64 object-cover"
                  />
                ) : (
                  <div className="w-full h-64 bg-slate-700 flex items-center justify-center">
                    <Film className="h-16 w-16 text-gray-500" />
                  </div>
                )}
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-white mb-1">{movie.title}</h3>
                  {movie.year && (
                    <p className="text-sm text-gray-400 mb-2">{movie.year}</p>
                  )}
                  {movie.imdb_rating && (
                    <div className="flex items-center">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      <span className="text-sm text-gray-300">{movie.imdb_rating}/10</span>
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

