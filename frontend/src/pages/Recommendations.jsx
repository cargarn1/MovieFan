import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { moviesService } from '../services/movies';
import { Star, Film } from 'lucide-react';

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const data = await moviesService.getRecommendations();
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">Personalized Recommendations</h1>

      {loading ? (
        <div className="text-center text-gray-400 py-12">Loading recommendations...</div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400 mb-4">No recommendations available yet.</p>
          <p className="text-gray-500 text-sm">
            Update your preferences in your profile to get personalized recommendations.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {recommendations.map((rec) => (
            <Link
              key={rec.movie.id}
              to={`/movies/${rec.movie.id}`}
              className="bg-slate-800 rounded-lg overflow-hidden hover:bg-slate-700 transition-colors"
            >
              {rec.movie.poster_url ? (
                <img
                  src={rec.movie.poster_url}
                  alt={rec.movie.title}
                  className="w-full h-80 object-cover"
                />
              ) : (
                <div className="w-full h-80 bg-slate-700 flex items-center justify-center">
                  <Film className="h-16 w-16 text-gray-500" />
                </div>
              )}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-white mb-2">{rec.movie.title}</h3>
                {rec.movie.year && (
                  <p className="text-sm text-gray-400 mb-2">{rec.movie.year}</p>
                )}
                <div className="flex items-center mb-2">
                  {rec.movie.imdb_rating && (
                    <div className="flex items-center mr-4">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      <span className="text-sm text-gray-300">{rec.movie.imdb_rating}</span>
                    </div>
                  )}
                </div>
                <p className="text-sm text-primary-400 italic">{rec.reason}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

