import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { roomsService } from '../services/rooms';
import { Users, Film } from 'lucide-react';

export default function MyRooms() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    setLoading(true);
    try {
      const data = await roomsService.getMyRooms();
      setRooms(data);
    } catch (error) {
      console.error('Failed to load rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">My Rooms</h1>

      {loading ? (
        <div className="text-center text-gray-400 py-12">Loading your rooms...</div>
      ) : rooms.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400 mb-4">You haven't joined any rooms yet.</p>
          <Link
            to="/rooms"
            className="inline-block px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Browse Rooms
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {rooms.map((room) => (
            <Link
              key={room.id}
              to={`/rooms/${room.id}`}
              className="bg-slate-800 rounded-lg p-6 hover:bg-slate-700 transition-colors"
            >
              <h3 className="text-xl font-semibold text-white mb-2">{room.name}</h3>
              {room.description && (
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">{room.description}</p>
              )}
              {room.movie && (
                <div className="flex items-center text-sm text-gray-400 mb-4">
                  <Film className="h-4 w-4 mr-2" />
                  {room.movie.title}
                </div>
              )}
              <div className="flex items-center text-sm text-gray-400">
                <Users className="h-4 w-4 mr-1" />
                {room.member_count || 0} members
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}


