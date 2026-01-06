const perform = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/movies`,
    method: 'GET',
    headers: {
      'X-API-Key': bundle.authData.apiKey
    },
    params: {
      search: bundle.inputData.search,
      limit: bundle.inputData.limit || 20
    }
  });
  return response.json;
};

module.exports = {
  key: 'searchMovies',
  noun: 'Movie',
  display: {
    label: 'Search Movies',
    description: 'Searches for movies in MovieFan.'
  },
  operation: {
    inputFields: [
      {
        key: 'search',
        label: 'Search Query',
        type: 'string',
        required: true
      },
      {
        key: 'limit',
        label: 'Limit',
        type: 'integer',
        required: false
      }
    ],
    perform,
    sample: {
      id: 1,
      title: 'The Shawshank Redemption',
      year: 1994,
      genre: 'Drama',
      director: 'Frank Darabont',
      imdb_rating: '9.3'
    }
  }
};

