import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { moviesService } from '../services/movies';
import { reviewsService } from '../services/reviews';
import { roomsService } from '../services/rooms';
import { Star, Users, MessageSquare, Plus, Film } from 'lucide-react';
import { authService } from '../services/auth';

export default function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [movieReviews, setMovieReviews] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewText, setReviewText] = useState('');
  const [showReviewForm, setShowReviewForm] = useState(false);
  const isAuthenticated = authService.isAuthenticated();

  useEffect(() => {
    loadMovieData();
  }, [id]);

  const loadMovieData = async () => {
    setLoading(true);
    try {
      const [movieData, reviewsData, roomsData] = await Promise.all([
        moviesService.get(id),
        reviewsService.getByMovie(id),
        roomsService.list({ movie_id: parseInt(id) }),
      ]);
      setMovie(movieData);
      setMovieReviews(reviewsData);
      setRooms(roomsData);
    } catch (error) {
      console.error('Failed to load movie data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      alert('Please login to submit a review');
      return;
    }

    try {
      await reviewsService.create({
        movie_id: parseInt(id),
        rating: reviewRating,
        review_text: reviewText,
      });
      setReviewText('');
      setShowReviewForm(false);
      loadMovieData();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to submit review');
    }
  };

  if (loading) {
    return <div className="text-center text-gray-400 py-12">Loading...</div>;
  }

  if (!movie) {
    return <div className="text-center text-gray-400 py-12">Movie not found</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div className="lg:col-span-1">
          {movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="w-full rounded-lg"
            />
          ) : (
            <div className="w-full h-96 bg-slate-800 rounded-lg flex items-center justify-center">
              <Film className="h-24 w-24 text-gray-500" />
            </div>
          )}
        </div>
        <div className="lg:col-span-2">
          <h1 className="text-4xl font-bold text-white mb-4">{movie.title}</h1>
          {movie.year && <p className="text-xl text-gray-400 mb-4">{movie.year}</p>}
          
          <div className="flex items-center gap-4 mb-4">
            {movie.imdb_rating && (
              <div className="flex items-center">
                <Star className="h-5 w-5 text-yellow-400 mr-1" />
                <span className="text-white">IMDB: {movie.imdb_rating}</span>
              </div>
            )}
            {movie.average_rating && (
              <div className="flex items-center">
                <Star className="h-5 w-5 text-primary-400 mr-1" />
                <span className="text-white">Average: {movie.average_rating}</span>
              </div>
            )}
          </div>

          {movie.genre && (
            <div className="mb-4">
              <span className="text-sm text-gray-400">Genres: </span>
              <span className="text-white">{movie.genre}</span>
            </div>
          )}

          {movie.director && (
            <div className="mb-4">
              <span className="text-sm text-gray-400">Director: </span>
              <span className="text-white">{movie.director}</span>
            </div>
          )}

          {movie.plot && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-white mb-2">Plot</h3>
              <p className="text-gray-300">{movie.plot}</p>
            </div>
          )}

          {isAuthenticated && (
            <Link
              to={`/rooms/create?movie_id=${id}`}
              className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Room for this Movie
            </Link>
          )}
        </div>
      </div>

      {/* Rooms Section */}
      {rooms.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
            <Users className="h-6 w-6 mr-2" />
            Discussion Rooms ({rooms.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {rooms.map((room) => (
              <Link
                key={room.id}
                to={`/rooms/${room.id}`}
                className="bg-slate-800 rounded-lg p-4 hover:bg-slate-700 transition-colors"
              >
                <h3 className="text-lg font-semibold text-white mb-2">{room.name}</h3>
                {room.description && (
                  <p className="text-gray-400 text-sm mb-2">{room.description}</p>
                )}
                <p className="text-sm text-gray-500">
                  {room.member_count || 0} members
                </p>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Reviews Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <MessageSquare className="h-6 w-6 mr-2" />
            Reviews ({movieReviews.length})
          </h2>
          {isAuthenticated && !showReviewForm && (
            <button
              onClick={() => setShowReviewForm(true)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Write Review
            </button>
          )}
        </div>

        {showReviewForm && (
          <form onSubmit={handleSubmitReview} className="bg-slate-800 rounded-lg p-6 mb-6">
            <div className="mb-4">
              <label className="block text-white mb-2">Rating (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                value={reviewRating}
                onChange={(e) => setReviewRating(parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded text-white"
              />
            </div>
            <div className="mb-4">
              <label className="block text-white mb-2">Review</label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded text-white"
                placeholder="Write your review..."
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                Submit Review
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowReviewForm(false);
                  setReviewText('');
                }}
                className="px-4 py-2 bg-slate-700 text-white rounded hover:bg-slate-600"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        <div className="space-y-4">
          {movieReviews.length === 0 ? (
            <p className="text-gray-400">No reviews yet. Be the first to review!</p>
          ) : (
            movieReviews.map((review) => (
              <div key={review.id} className="bg-slate-800 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <Star className="h-5 w-5 text-yellow-400 mr-1" />
                    <span className="text-white font-semibold">{review.rating}/10</span>
                    {review.user && (
                      <span className="text-gray-400 ml-2">by {review.user.username}</span>
                    )}
                  </div>
                </div>
                {review.review_text && (
                  <p className="text-gray-300">{review.review_text}</p>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

