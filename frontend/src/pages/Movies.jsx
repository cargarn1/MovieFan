import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { moviesService } from '../services/movies';
import { Search, Film, Star } from 'lucide-react';

export default function Movies() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadMovies();
  }, [searchTerm, currentPage]);

  const loadMovies = async () => {
    setLoading(true);
    try {
      const params = {
        limit: 20,
        skip: (currentPage - 1) * 20,
      };
      if (searchTerm) {
        params.search = searchTerm;
      }
      const data = await moviesService.list(params);
      setMovies(data);
    } catch (error) {
      console.error('Failed to load movies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadMovies();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-4">Movies</h1>
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search movies..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Search
          </button>
        </form>
      </div>

      {loading ? (
        <div className="text-center text-gray-400 py-12">Loading movies...</div>
      ) : movies.length === 0 ? (
        <div className="text-center text-gray-400 py-12">
          No movies found. Try a different search term.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
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
                  className="w-full h-80 object-cover"
                />
              ) : (
                <div className="w-full h-80 bg-slate-700 flex items-center justify-center">
                  <Film className="h-16 w-16 text-gray-500" />
                </div>
              )}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-white mb-1 line-clamp-2">
                  {movie.title}
                </h3>
                {movie.year && <p className="text-sm text-gray-400 mb-2">{movie.year}</p>}
                <div className="flex items-center justify-between">
                  {movie.imdb_rating && (
                    <div className="flex items-center">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      <span className="text-sm text-gray-300">{movie.imdb_rating}</span>
                    </div>
                  )}
                  {movie.average_rating && (
                    <span className="text-sm text-primary-400">
                      {movie.average_rating} avg
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

