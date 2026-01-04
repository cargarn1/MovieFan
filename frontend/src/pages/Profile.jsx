import { useState } from 'react';
import { Key } from 'lucide-react';
import { usersService } from '../services/users';

export default function Profile({ user: initialUser }) {
  const [user, setUser] = useState(initialUser);
  const [apiKey, setApiKey] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);

  const loadApiKey = async () => {
    try {
      const response = await usersService.getApiKey();
      setApiKey(response.api_key);
      setShowApiKey(true);
    } catch (error) {
      console.error('Failed to load API key:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-slate-800 rounded-lg p-6 mb-6">
        <div className="flex items-center mb-6">
          <div className="h-16 w-16 rounded-full bg-primary-600 flex items-center justify-center text-white text-2xl font-bold mr-4">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{user.username}</h1>
            {user.full_name && (
              <p className="text-gray-400">{user.full_name}</p>
            )}
            {user.email && (
              <p className="text-sm text-gray-500">{user.email}</p>
            )}
          </div>
        </div>

        {user.bio && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-2">Bio</h3>
            <p className="text-gray-300">{user.bio}</p>
          </div>
        )}
      </div>

      <div className="bg-slate-800 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <Key className="h-5 w-5 mr-2" />
            API Key (for Zapier)
          </h2>
          {!showApiKey && (
            <button
              onClick={loadApiKey}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Get API Key
            </button>
          )}
        </div>

        {showApiKey && (
          <div>
            <p className="text-sm text-gray-400 mb-2">
              Use this API key in Zapier integrations:
            </p>
            <div className="bg-slate-900 rounded p-3 mb-4">
              <code className="text-primary-400 break-all">{apiKey}</code>
            </div>
            <p className="text-xs text-gray-500">
              Keep this key secure. Don't share it publicly.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

