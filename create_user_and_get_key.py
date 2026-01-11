#!/usr/bin/env python3
"""Helper script to create a user and get API key."""
import sys
import requests
import json

API_URL = "http://localhost:5001"

def create_user_and_get_api_key(username, email, password, full_name):
    """Create a user and get their API key."""
    
    # Step 1: Try to register
    print(f"Attempting to register user: {username}...")
    try:
        register_response = requests.post(
            f"{API_URL}/api/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "full_name": full_name
            }
        )
        
        if register_response.status_code == 201:
            print("✓ User registered successfully!")
        elif register_response.status_code == 400:
            error_detail = register_response.json().get("detail", "Unknown error")
            if "already registered" in error_detail:
                print(f"✓ User already exists: {error_detail}")
            else:
                print(f"✗ Registration failed: {error_detail}")
                return None
        else:
            print(f"✗ Registration failed with status {register_response.status_code}")
            print(f"Response: {register_response.text[:200]}")
            return None
    except Exception as e:
        print(f"✗ Error during registration: {e}")
        return None
    
    # Step 2: Login to get JWT token
    print(f"\nLogging in as {username}...")
    try:
        login_response = requests.post(
            f"{API_URL}/api/auth/login",
            data={
                "username": username,
                "password": password
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code != 200:
            print(f"✗ Login failed: {login_response.text}")
            return None
        
        token_data = login_response.json()
        token = token_data.get("access_token")
        
        if not token:
            print("✗ No access token received")
            return None
        
        print("✓ Login successful!")
    except Exception as e:
        print(f"✗ Error during login: {e}")
        return None
    
    # Step 3: Get or create API key
    print(f"\nGetting API key...")
    try:
        api_key_response = requests.get(
            f"{API_URL}/api/zapier/api-key",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if api_key_response.status_code != 200:
            print(f"✗ Failed to get API key: {api_key_response.text}")
            return None
        
        api_key_data = api_key_response.json()
        api_key = api_key_data.get("api_key")
        
        if not api_key:
            print("✗ No API key received")
            return None
        
        print("✓ API key retrieved!")
        return api_key
        
    except Exception as e:
        print(f"✗ Error getting API key: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        username = sys.argv[1]
        email = sys.argv[2]
        password = sys.argv[3]
        full_name = sys.argv[4] if len(sys.argv) > 4 else username
    else:
        print("Usage: python3 create_user_and_get_key.py <username> <email> <password> [full_name]")
        print("\nExample:")
        print("  python3 create_user_and_get_key.py cargarn1 cargarn1@example.com changeme123 'Carlos Garcia'")
        sys.exit(1)
    
    api_key = create_user_and_get_api_key(username, email, password, full_name)
    
    if api_key:
        print("\n" + "="*60)
        print("YOUR API KEY FOR ZAPIER:")
        print("="*60)
        print(api_key)
        print("="*60)
        print(f"\nAPI URL: {API_URL}")
        print("Use this header in Zapier: X-API-Key")
        print("="*60)
    else:
        print("\n✗ Failed to get API key. Please check the errors above.")
        sys.exit(1)


