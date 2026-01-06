const performSubscribe = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/webhooks`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey,
      'Content-Type': 'application/json'
    },
    body: {
      event_type: 'new_room',
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
  // For webhook triggers, this is called when Zapier needs to verify the hook
  // Return empty array as webhooks handle data delivery
  return [];
};

module.exports = {
  key: 'newRoom',
  noun: 'Room',
  display: {
    label: 'New Room',
    description: 'Triggers when a new room is created in MovieFan.'
  },
  operation: {
    type: 'hook',
    performSubscribe,
    performUnsubscribe,
    perform,
    sample: {
      event: 'new_room',
      room_id: 1,
      room_name: 'The Matrix Discussion',
      movie_id: 6,
      movie_title: 'The Matrix',
      creator_id: 1,
      created_at: '2024-01-01T00:00:00Z'
    }
  }
};


