import requests
import pytest

class TestHabiticaPublicAPI:
    """Simple tests for Habitica public API endpoints - Updated based on actual responses"""
    
    BASE_URL = "https://habitica.com/api/v3"
    
    def test_api_status(self):
        """Test the basic API status endpoint"""
        print("Testing API status endpoint...")
        response = requests.get(f"{self.BASE_URL}/status")
        
        # Check response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        print(f"Status Response: {data}")
        
        # Validate response structure
        assert data['success'] == True
        assert data['data']['status'] == 'up'
        
        # Handle optional fields gracefully
        if 'appVersion' in data['data']:
            print(f"✅ API Status: {data['data']['status']} (Version: {data['data']['appVersion']})")
        else:
            print(f"✅ API Status: {data['data']['status']}")
    
    
    
    def test_world_state(self):
        """Test world state endpoint"""
        print("Testing world state endpoint...")
        response = requests.get(f"{self.BASE_URL}/world-state")
        
        # Check response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        print(f"World State Response: {data}")
        
        # Validate response structure
        assert data['success'] == True
        assert 'data' in data
        
        world_data = data['data']
        if 'worldDrops' in world_data:
            print("✅ World State: Contains world drops data")
        elif 'npc' in world_data:
            print("✅ World State: Contains NPC data")
        else:
            print("✅ World State: Responded with valid structure")
    
    def test_api_error_handling(self):
        """Test how the API handles invalid requests"""
        print("Testing API error handling...")
        
        # Test with invalid endpoint
        response = requests.get(f"{self.BASE_URL}/invalid-endpoint")
        
        # Should return an error, but let's see what we get
        print(f"Invalid endpoint response: {response.status_code}")
        
        # The API might return 404, 400, or other error codes
        assert response.status_code >= 400, f"Expected error code, got {response.status_code}"
        
        if response.status_code == 404:
            print("✅ Error Handling: Proper 404 for invalid endpoint")
        else:
            data = response.json()
            print(f"✅ Error Handling: API returned {response.status_code} with message: {data.get('error', 'Unknown error')}")
    
    def test_api_headers(self):
        """Test that API returns proper headers"""
        print("Testing API headers...")
        response = requests.get(f"{self.BASE_URL}/status")
        
        # Check important headers
        assert 'Content-Type' in response.headers
        assert 'application/json' in response.headers['Content-Type']
        
        print(f"✅ Headers: Content-Type = {response.headers['Content-Type']}")
        
        # Check for CORS headers if present
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"✅ CORS: {response.headers['Access-Control-Allow-Origin']}")

def test_api_response_time():
    """Test API response time performance"""
    import time
    
    start_time = time.time()
    response = requests.get("https://habitica.com/api/v3/status")
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 10.0, f"Response time too slow: {response_time:.2f}s"
    
    print(f"✅ Performance: Response time {response_time:.2f} seconds")