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
      helpText: 'Get your API key from MovieFan. Login at http://localhost:5001, then visit http://localhost:5001/api/zapier/api-key'
    },
    {
      key: 'apiUrl',
      label: 'API URL',
      type: 'string',
      required: true,
      default: 'http://localhost:5001',
      helpText: 'Your MovieFan API base URL (use http://localhost:5001 for local development)'
    }
  ]
};

module.exports = authentication;


