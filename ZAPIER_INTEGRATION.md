# Zapier Integration Guide

This guide will help you integrate MovieFan API with Zapier using `zapier-platform-cli`.

## Overview

MovieFan API supports Zapier integration through:
- **API Key Authentication** - Simple API key-based auth for Zapier
- **Webhook Triggers** - Real-time notifications for events
- **Action Endpoints** - Create/search operations optimized for Zapier

## Setup

### 1. Get Your API Key

First, authenticate and get your API key:

```bash
# Login to get JWT token
curl -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"

# Get or create API key
curl -X GET "http://localhost:5001/api/zapier/api-key" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "api_key": "your-api-key-here",
  "message": "Use this API key in Zapier: X-API-Key header"
}
```

### 2. Test Connection

Test your API key:

```bash
curl -X GET "http://localhost:5001/api/zapier/test" \
  -H "X-API-Key: your-api-key-here"
```

## Zapier App Structure

Create your Zapier app structure:

```bash
zapier init movie-fan
cd movie-fan
```

## Authentication

In your Zapier app's `authentication.js`:

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
      helpText: 'Get your API key from MovieFan API'
    },
    {
      key: 'apiUrl',
      label: 'API URL',
      type: 'string',
      required: true,
      default: 'http://localhost:5001',
      helpText: 'Your MovieFan API base URL'
    }
  ]
};

module.exports = authentication;
```

## Triggers

### 1. New Room Trigger

Create `triggers/newRoom.js`:

```javascript
const perform = async (z, bundle) => {
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

module.exports = {
  key: 'newRoom',
  noun: 'Room',
  display: {
    label: 'New Room',
    description: 'Triggers when a new room is created.'
  },
  operation: {
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

### 2. New Review Trigger

Create `triggers/newReview.js`:

```javascript
const perform = async (z, bundle) => {
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

module.exports = {
  key: 'newReview',
  noun: 'Review',
  display: {
    label: 'New Review',
    description: 'Triggers when a new review is posted.'
  },
  operation: {
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

## Actions

### 1. Create Room Action

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

### 2. Create Review Action

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

### 3. Search Movies Action

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

## API Endpoints Reference

### Authentication
- `GET /api/zapier/api-key` - Get or create API key
- `GET /api/zapier/test` - Test connection

### Webhooks
- `POST /api/zapier/webhooks` - Create webhook subscription
- `GET /api/zapier/webhooks` - List webhook subscriptions
- `DELETE /api/zapier/webhooks/{id}` - Delete webhook subscription

### Actions
- `POST /api/zapier/rooms` - Create room
- `GET /api/zapier/rooms` - List rooms
- `POST /api/zapier/reviews` - Create review
- `GET /api/zapier/reviews` - List reviews
- `GET /api/zapier/movies` - List/search movies

## Webhook Events

### Event Types
- `new_room` - Triggered when a new room is created
- `new_review` - Triggered when a new review is posted
- `new_movie` - Triggered when a new movie is imported
- `room_joined` - Triggered when a user joins a room

### Webhook Payload Format

**New Room:**
```json
{
  "event": "new_room",
  "room_id": 1,
  "room_name": "The Matrix Discussion",
  "movie_id": 6,
  "movie_title": "The Matrix",
  "creator_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**New Review:**
```json
{
  "event": "new_review",
  "review_id": 1,
  "movie_id": 1,
  "movie_title": "The Shawshank Redemption",
  "rating": 9,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Testing Your Zapier App

1. **Test Authentication:**
```bash
zapier test auth
```

2. **Test Triggers:**
```bash
zapier test trigger newRoom
zapier test trigger newReview
```

3. **Test Actions:**
```bash
zapier test create createRoom
zapier test create createReview
zapier test search searchMovies
```

4. **Push to Zapier:**
```bash
zapier push
```

## Example Zap Scenarios

### Scenario 1: Notify Slack when New Room Created
- **Trigger:** New Room
- **Action:** Send Slack Message with room details

### Scenario 2: Create Google Sheet Row for New Reviews
- **Trigger:** New Review
- **Action:** Create Google Sheets Row with review data

### Scenario 3: Auto-create Room from New Movie Import
- **Trigger:** New Movie (from TMDB import)
- **Action:** Create Room for the movie

## Production Considerations

1. **API URL:** Update `apiUrl` to your production API URL
2. **HTTPS:** Use HTTPS for webhooks in production
3. **Rate Limiting:** Implement rate limiting for API endpoints
4. **Error Handling:** Add proper error handling in Zapier app
5. **Webhook Security:** Use webhook secrets for verification

## Support

For issues or questions:
- Check API docs: `http://localhost:5001/docs`
- Review Zapier platform docs: https://platform.zapier.com/docs

