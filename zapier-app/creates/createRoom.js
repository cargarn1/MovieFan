const perform = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/rooms`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey,
      'Content-Type': 'application/json'
    },
    body: {
      name: bundle.inputData.name,
      movie_id: bundle.inputData.movie_id,
      description: bundle.inputData.description,
      is_private: bundle.inputData.is_private || false,
      max_members: bundle.inputData.max_members || 50
    }
  });
  return response.json;
};

module.exports = {
  key: 'createRoom',
  noun: 'Room',
  display: {
    label: 'Create Room',
    description: 'Creates a new movie discussion room.'
  },
  operation: {
    inputFields: [
      {
        key: 'name',
        label: 'Room Name',
        type: 'string',
        required: true
      },
      {
        key: 'movie_id',
        label: 'Movie ID',
        type: 'integer',
        required: true,
        helpText: 'The ID of the movie for this room'
      },
      {
        key: 'description',
        label: 'Description',
        type: 'text',
        required: false
      },
      {
        key: 'is_private',
        label: 'Private Room',
        type: 'boolean',
        required: false
      },
      {
        key: 'max_members',
        label: 'Max Members',
        type: 'integer',
        required: false
      }
    ],
    perform,
    sample: {
      id: 1,
      name: 'The Matrix Discussion',
      movie_id: 6,
      description: 'Let\'s discuss The Matrix!',
      creator_id: 1,
      is_private: false,
      max_members: 50,
      created_at: '2024-01-01T00:00:00Z'
    }
  }
};

