#!/usr/bin/env python3
"""Quick test script for MovieFan API."""
import requests
import json
import sys

BASE_URL = "http://localhost:5001"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_endpoint(method, endpoint, description, headers=None, data=None, expected_status=200):
    """Test an API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{description}...")
    print(f"  {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        if response.status_code == expected_status:
            print(f"  ✓ Success ({response.status_code})")
            try:
                result = response.json()
                if isinstance(result, dict) and len(result) < 5:
                    print(f"  Response: {json.dumps(result, indent=2)}")
                elif isinstance(result, list) and len(result) < 3:
                    print(f"  Response: {json.dumps(result, indent=2)}")
                else:
                    print(f"  Response: {type(result).__name__} with {len(result) if isinstance(result, (list, dict)) else 'data'}")
            except:
                print(f"  Response: {response.text[:100]}")
            return response
        else:
            print(f"  ✗ Failed ({response.status_code})")
            print(f"  Error: {response.text[:200]}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Connection Error - Is the server running on {BASE_URL}?")
        return None
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return None

def main():
    print_section("MovieFan API Test Suite")
    
    # Check if server is running
    print("\nChecking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=2)
        print("✓ Server is running")
    except:
        print("✗ Server is not running!")
        print(f"  Please start the server: python run.py")
        sys.exit(1)
    
    # Test 1: Register user
    print_section("1. Authentication Tests")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    register_response = test_endpoint("POST", "/api/auth/register", "Register new user", data=register_data)
    
    if not register_response:
        print("\n  Note: User might already exist, trying login...")
    
    # Test 2: Login
    login_response = test_endpoint(
        "POST",
        "/api/auth/login",
        "Login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "testuser", "password": "testpass123"}
    )
    
    if not login_response:
        print("\n✗ Cannot continue without authentication token")
        sys.exit(1)
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"\n  Token received: {token[:20]}...")
    
    # Test 3: Get current user
    test_endpoint("GET", "/api/auth/me", "Get current user info", headers=headers)
    
    # Test 4: TMDB Integration
    print_section("2. TMDB Integration Tests")
    test_endpoint("GET", "/api/tmdb/search?query=inception", "Search TMDB for 'Inception'")
    test_endpoint("GET", "/api/tmdb/popular?page=1", "Get popular movies from TMDB")
    test_endpoint("GET", "/api/tmdb/top-rated?page=1", "Get top-rated movies from TMDB")
    
    # Test 5: Import movie from TMDB
    import_response = test_endpoint(
        "POST",
        "/api/tmdb/import/27205",  # Inception TMDB ID
        "Import Inception from TMDB",
        headers=headers,
        expected_status=201
    )
    
    movie_id = 1  # Default fallback
    if import_response:
        movie_data = import_response.json()
        movie_id = movie_data.get("id", 1)
        print(f"\n  Imported movie ID: {movie_id}")
    
    # Test 6: Movies
    print_section("3. Movie Management Tests")
    test_endpoint("GET", "/api/movies", "List all movies")
    test_endpoint("GET", f"/api/movies/{movie_id}", f"Get movie details (ID: {movie_id})")
    test_endpoint("GET", "/api/movies/recommendations/me", "Get recommendations", headers=headers)
    
    # Test 7: Reviews
    print_section("4. Review & Rating Tests")
    review_data = {
        "movie_id": movie_id,
        "rating": 9,
        "review_text": "Amazing movie! One of my favorites."
    }
    review_response = test_endpoint(
        "POST",
        "/api/reviews",
        "Create a review",
        headers=headers,
        data=review_data,
        expected_status=201
    )
    
    review_id = None
    if review_response:
        review_data = review_response.json()
        review_id = review_data.get("id")
        print(f"\n  Created review ID: {review_id}")
    
    test_endpoint("GET", f"/api/reviews/movie/{movie_id}", f"Get reviews for movie {movie_id}")
    test_endpoint("GET", "/api/reviews/me", "Get my reviews", headers=headers)
    
    # Test 8: Rooms
    print_section("5. Room Management Tests")
    room_data = {
        "name": "Inception Discussion",
        "description": "Let's discuss Inception!",
        "movie_id": movie_id,
        "is_private": False
    }
    room_response = test_endpoint(
        "POST",
        "/api/rooms",
        "Create a room",
        headers=headers,
        data=room_data,
        expected_status=201
    )
    
    room_id = None
    if room_response:
        room_data = room_response.json()
        room_id = room_data.get("id")
        print(f"\n  Created room ID: {room_id}")
    
    test_endpoint("GET", "/api/rooms", "List all rooms", headers=headers)
    test_endpoint("GET", "/api/rooms/my-rooms", "Get my rooms", headers=headers)
    
    if room_id:
        test_endpoint("POST", f"/api/rooms/{room_id}/join", "Join room", headers=headers)
    
    # Test 9: User Preferences
    print_section("6. User Preferences Tests")
    preferences_data = {
        "favorite_genres": "Action,Sci-Fi,Drama",
        "favorite_directors": "Christopher Nolan",
        "favorite_actors": "Leonardo DiCaprio",
        "min_rating": 7,
        "preferred_decades": "2000s,2010s"
    }
    test_endpoint(
        "PUT",
        "/api/users/me/preferences",
        "Update preferences",
        headers=headers,
        data=preferences_data
    )
    test_endpoint("GET", "/api/users/me/preferences", "Get preferences", headers=headers)
    
    # Test 10: Zapier Integration
    print_section("7. Zapier Integration Tests")
    test_endpoint("GET", "/api/zapier/api-key", "Get API key", headers=headers)
    test_endpoint("GET", "/api/zapier/test", "Test Zapier connection", headers=headers)
    
    print_section("Test Suite Complete!")
    print("\n✓ All tests completed!")
    print(f"\nNext steps:")
    print(f"  - Check the API docs at: {BASE_URL}/docs")
    print(f"  - Test the frontend at: http://localhost:5000")
    print(f"  - See TESTING.md for more detailed testing instructions")

if __name__ == "__main__":
    main()
