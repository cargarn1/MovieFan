import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { roomsService } from '../services/rooms';
import { Users, Film, UserPlus } from 'lucide-react';
import { authService } from '../services/auth';

export default function RoomDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isMember, setIsMember] = useState(false);
  const isAuthenticated = authService.isAuthenticated();

  useEffect(() => {
    loadRoom();
  }, [id]);

  const loadRoom = async () => {
    setLoading(true);
    try {
      const roomData = await roomsService.get(id);
      setRoom(roomData);
      // Check if current user is a member
      if (isAuthenticated) {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        setIsMember(roomData.members?.some(m => m.id === user.id) || false);
      }
    } catch (error) {
      console.error('Failed to load room:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      await roomsService.join(id);
      loadRoom();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to join room');
    }
  };

  const handleLeave = async () => {
    try {
      await roomsService.leave(id);
      loadRoom();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to leave room');
    }
  };

  if (loading) {
    return <div className="text-center text-gray-400 py-12">Loading...</div>;
  }

  if (!room) {
    return <div className="text-center text-gray-400 py-12">Room not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-slate-800 rounded-lg p-6 mb-6">
        <h1 className="text-3xl font-bold text-white mb-4">{room.name}</h1>
        {room.description && (
          <p className="text-gray-300 mb-4">{room.description}</p>
        )}
        
        {room.movie && (
          <Link
            to={`/movies/${room.movie.id}`}
            className="inline-flex items-center text-primary-400 hover:text-primary-300 mb-4"
          >
            <Film className="h-5 w-5 mr-2" />
            {room.movie.title}
          </Link>
        )}

        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center text-gray-400">
            <Users className="h-5 w-5 mr-2" />
            {room.member_count || 0} members
          </div>
          {isAuthenticated && (
            <div>
              {isMember ? (
                <button
                  onClick={handleLeave}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                  Leave Room
                </button>
              ) : (
                <button
                  onClick={handleJoin}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center"
                >
                  <UserPlus className="h-4 w-4 mr-2" />
                  Join Room
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {room.members && room.members.length > 0 && (
        <div className="bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Members</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {room.members.map((member) => (
              <div key={member.id} className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold mr-3">
                  {member.username.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="text-white font-medium">{member.username}</p>
                  {member.full_name && (
                    <p className="text-sm text-gray-400">{member.full_name}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}



