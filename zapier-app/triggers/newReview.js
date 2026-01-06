const performSubscribe = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/webhooks`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey,
      'Content-Type': 'application/json'
    },
    body: {
      event_type: 'new_review',
      webhook_url: bundle.targetUrl
    }
  });
  return response.json;
};

const performUnsubscribe = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/webhooks`,
    method: 'GET',
    headers: {
      'X-API-Key': bundle.authData.apiKey
    }
  });
  
  const subscriptions = response.json;
  const subscription = subscriptions.find(sub => sub.webhook_url === bundle.targetUrl);
  
  if (subscription) {
    await z.request({
      url: `${bundle.authData.apiUrl}/api/zapier/webhooks/${subscription.id}`,
      method: 'DELETE',
      headers: {
        'X-API-Key': bundle.authData.apiKey
      }
    });
  }
  
  return {};
};

const perform = async (z, bundle) => {
  return [];
};

module.exports = {
  key: 'newReview',
  noun: 'Review',
  display: {
    label: 'New Review',
    description: 'Triggers when a new review is posted in MovieFan.'
  },
  operation: {
    type: 'hook',
    performSubscribe,
    performUnsubscribe,
    perform,
    sample: {
      event: 'new_review',
      review_id: 1,
      movie_id: 1,
      movie_title: 'The Shawshank Redemption',
      rating: 9,
      user_id: 1,
      created_at: '2024-01-01T00:00:00Z'
    }
  }
};


