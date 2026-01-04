import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { roomsService } from '../services/rooms';
import { Users, Search, Film } from 'lucide-react';

export default function Rooms() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadRooms();
  }, [searchTerm]);

  const loadRooms = async () => {
    setLoading(true);
    try {
      const params = {};
      if (searchTerm) {
        params.search = searchTerm;
      }
      const data = await roomsService.list(params);
      setRooms(data);
    } catch (error) {
      console.error('Failed to load rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-4">Discussion Rooms</h1>
        <form onSubmit={(e) => { e.preventDefault(); loadRooms(); }} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search rooms..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </form>
      </div>

      {loading ? (
        <div className="text-center text-gray-400 py-12">Loading rooms...</div>
      ) : rooms.length === 0 ? (
        <div className="text-center text-gray-400 py-12">
          No rooms found. Create one to get started!
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
              <div className="flex items-center justify-between">
                <div className="flex items-center text-sm text-gray-400">
                  <Users className="h-4 w-4 mr-1" />
                  {room.member_count || 0} members
                </div>
                {room.is_private && (
                  <span className="text-xs bg-slate-700 text-gray-300 px-2 py-1 rounded">
                    Private
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

