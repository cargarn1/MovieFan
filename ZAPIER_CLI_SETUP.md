# Zapier CLI Setup Guide for MovieFan

Complete step-by-step guide to create a Zapier integration using `zapier-platform-cli`.

## Prerequisites

1. **Node.js installed** ✅ (You have v24.12.0)
2. **Zapier account** - Sign up at https://zapier.com
3. **MovieFan API running** - Backend on port 8001

## Step 1: Install Zapier CLI

```bash
npm install -g zapier-platform-cli
```

Verify installation:
```bash
zapier --version
```

## Step 2: Login to Zapier

```bash
zapier login
```

This will open your browser to authenticate. After logging in, you'll be authenticated in the CLI.

## Step 3: Initialize Zapier App

Create a new directory for your Zapier app (outside MovieFan project):

```bash
cd ~/Documents/Code
zapier init movie-fan-zapier
cd movie-fan-zapier
```

This creates a new Zapier app with the basic structure.

## Step 4: Configure Authentication

Edit `authentication.js`:

```javascript
const authentication = {
  type: 'custom',
  test: {
    url: '{{bundle.authData.apiUrl}}/api/zapier/test',
    method: 'GET',
    headers: {
      'X-API-Key': '{{bundle.authData.apiKey}}'
    }
  },
  fields: [
    {
      key: 'apiKey',
      label: 'API Key',
      type: 'string',
      required: true,
      helpText: 'Get your API key from MovieFan: http://localhost:8001/api/zapier/api-key (after login)'
    },
    {
      key: 'apiUrl',
      label: 'API URL',
      type: 'string',
      required: true,
      default: 'http://localhost:8001',
      helpText: 'Your MovieFan API base URL'
    }
  ]
};

module.exports = authentication;
```

## Step 5: Create Triggers

### Trigger 1: New Room

Create `triggers/newRoom.js`:

```javascript
const performSubscribe = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/webhooks`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey
    },
    params: {
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
  // This is called when Zapier polls for new data
  // For webhooks, this might not be called, but it's required
  return [];
};

module.exports = {
  key: 'newRoom',
  noun: 'Room',
  display: {
    label: 'New Room',
    description: 'Triggers when a new room is created.'
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
```

### Trigger 2: New Review

Create `triggers/newReview.js`:

```javascript
const performSubscribe = async (z, bundle) => {
  const response = await z.request({
    url: `${bundle.authData.apiUrl}/api/zapier/webhooks`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.apiKey
    },
    params: {
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
    description: 'Triggers when a new review is posted.'
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
```

## Step 6: Create Actions

### Action 1: Create Room

Create `creates/createRoom.js`:

```javascript
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
        required: false,
        default: false
      },
      {
        key: 'max_members',
        label: 'Max Members',
        type: 'integer',
        required: false,
        default: 50
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
```

### Action 2: Create Review

Create `creates/createReview.js`:

```javascript
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
```

### Action 3: Search Movies

Create `searches/searchMovies.js`:

```javascript
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
    description: 'Searches for movies.'
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
        required: false,
        default: 20
      }
    ],
    perform,
    sample: [
      {
        id: 1,
        title: 'The Shawshank Redemption',
        year: 1994,
        genre: 'Drama',
        director: 'Frank Darabont',
        imdb_rating: '9.3'
      }
    ]
  }
};
```

## Step 7: Test Your Integration

### Test Authentication

```bash
zapier test auth
```

### Test a Trigger

```bash
zapier test trigger newRoom
```

### Test an Action

```bash
zapier test create createRoom
```

## Step 8: Register Your App

```bash
zapier register
```

This creates your app on Zapier's platform.

## Step 9: Push Your App

```bash
zapier push
```

This uploads your app to Zapier.

## Step 10: Invite Users (Optional)

```bash
zapier invite user@example.com
```

## Complete File Structure

Your Zapier app should have this structure:

```
movie-fan-zapier/
├── index.js              # Main app definition
├── package.json
├── authentication.js     # Auth configuration
├── triggers/
│   ├── newRoom.js
│   └── newReview.js
├── creates/
│   ├── createRoom.js
│   └── createReview.js
└── searches/
    └── searchMovies.js
```

## Testing Checklist

- [ ] Authentication works
- [ ] Triggers subscribe/unsubscribe correctly
- [ ] Actions create resources successfully
- [ ] Search returns results
- [ ] Webhooks receive events

## Next Steps

1. Test locally with `zapier test`
2. Push to Zapier with `zapier push`
3. Test in Zapier's web interface
4. Submit for public release (optional)


