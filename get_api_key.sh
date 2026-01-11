#!/bin/bash

# MovieFan API Key Retrieval Script
# This script helps you get your API key for Zapier integration

API_URL="http://localhost:5001"

echo "=== MovieFan API Key Retrieval ==="
echo ""

# Check if username and password are provided as arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./get_api_key.sh <username> <password>"
    echo ""
    echo "Example: ./get_api_key.sh myuser mypassword"
    echo ""
    echo "Or run interactively:"
    read -p "Username: " USERNAME
    read -sp "Password: " PASSWORD
    echo ""
else
    USERNAME=$1
    PASSWORD=$2
fi

echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${USERNAME}&password=${PASSWORD}")

# Check if login was successful
if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "✓ Login successful!"
    echo ""
    
    echo "Getting API key..."
    API_KEY_RESPONSE=$(curl -s -X GET "${API_URL}/api/zapier/api-key" \
      -H "Authorization: Bearer ${TOKEN}")
    
    if echo "$API_KEY_RESPONSE" | grep -q "api_key"; then
        API_KEY=$(echo "$API_KEY_RESPONSE" | grep -o '"api_key":"[^"]*' | cut -d'"' -f4)
        echo "✓ API Key retrieved!"
        echo ""
        echo "=========================================="
        echo "Your API Key for Zapier:"
        echo "=========================================="
        echo "$API_KEY"
        echo "=========================================="
        echo ""
        echo "Use this in Zapier with the header: X-API-Key"
        echo "API URL: ${API_URL}"
    else
        echo "✗ Failed to get API key"
        echo "Response: $API_KEY_RESPONSE"
    fi
else
    echo "✗ Login failed!"
    echo "Response: $LOGIN_RESPONSE"
    echo ""
    echo "Make sure:"
    echo "1. The backend server is running on port 5001"
    echo "2. You have registered an account"
    echo "3. Your username and password are correct"
fi

