const perform = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/reviews`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey,
      'Content-Type': 'application/json'
    },
    body: {
      movie_id: bundle.inputData.movie_id,
      rating: bundle.inputData.rating,
      review_text: bundle.inputData.review_text
    }
  });
  return response.json;
};

module.exports = {
  key: 'createReview',
  noun: 'Review',
  display: {
    label: 'Create Review',
    description: 'Creates a new movie review/rating.'
  },
  operation: {
    inputFields: [
      {
        key: 'movie_id',
        label: 'Movie ID',
        type: 'integer',
        required: true
      },
      {
        key: 'rating',
        label: 'Rating',
        type: 'integer',
        required: true,
        helpText: 'Rating from 1-10'
      },
      {
        key: 'review_text',
        label: 'Review Text',
        type: 'text',
        required: false
      }
    ],
    perform,
    sample: {
      id: 1,
      movie_id: 1,
      user_id: 1,
      rating: 9,
      review_text: 'Great movie!',
      created_at: '2024-01-01T00:00:00Z'
    }
  }
};



