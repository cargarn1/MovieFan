import { Link, useNavigate } from 'react-router-dom';
import { Film, Home, Users, Star, User, LogOut, Menu } from 'lucide-react';
import { useState } from 'react';

export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  return (
    <nav className="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center space-x-2 px-2 py-2 text-white hover:text-primary-400">
              <Film className="h-6 w-6" />
              <span className="text-xl font-bold">MovieFan</span>
            </Link>
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              <Link
                to="/"
                className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:border-b-2 hover:border-primary-500"
              >
                <Home className="h-4 w-4 mr-2" />
                Home
              </Link>
              <Link
                to="/movies"
                className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:border-b-2 hover:border-primary-500"
              >
                <Film className="h-4 w-4 mr-2" />
                Movies
              </Link>
              <Link
                to="/rooms"
                className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:border-b-2 hover:border-primary-500"
              >
                <Users className="h-4 w-4 mr-2" />
                Rooms
              </Link>
              {user && (
                <>
                  <Link
                    to="/recommendations"
                    className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:border-b-2 hover:border-primary-500"
                  >
                    <Star className="h-4 w-4 mr-2" />
                    Recommendations
                  </Link>
                  <Link
                    to="/my-rooms"
                    className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:border-b-2 hover:border-primary-500"
                  >
                    My Rooms
                  </Link>
                </>
              )}
            </div>
          </div>
          <div className="flex items-center">
            {user ? (
              <div className="hidden md:flex items-center space-x-4">
                <Link
                  to="/profile"
                  className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white"
                >
                  <User className="h-4 w-4 mr-2" />
                  {user.username}
                </Link>
                <button
                  onClick={handleLogout}
                  className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-300 hover:text-white"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </button>
              </div>
            ) : (
              <div className="hidden md:flex items-center space-x-4">
                <Link
                  to="/login"
                  className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 text-sm font-medium bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  Sign Up
                </Link>
              </div>
            )}
            <button
              className="md:hidden text-gray-300 hover:text-white"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-700">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              to="/"
              className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/movies"
              className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
              onClick={() => setMobileMenuOpen(false)}
            >
              Movies
            </Link>
            <Link
              to="/rooms"
              className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
              onClick={() => setMobileMenuOpen(false)}
            >
              Rooms
            </Link>
            {user ? (
              <>
                <Link
                  to="/recommendations"
                  className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Recommendations
                </Link>
                <Link
                  to="/my-rooms"
                  className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  My Rooms
                </Link>
                <Link
                  to="/profile"
                  className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Profile
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="block w-full text-left px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-3 py-2 text-base font-medium text-gray-300 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}



