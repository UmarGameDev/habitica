import pytest
import requests
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test_utils import HabiticaAPI, TestDataValidator
from config import config

class TestPublicAPI:
    @pytest.fixture
    def api_client(self):
        return HabiticaAPI()
    
    @pytest.fixture
    def validator(self):
        return TestDataValidator()
    
    def test_api_status_endpoint(self, api_client, validator):
        """Test the public status endpoint"""
        print("Testing API status endpoint...")
        
        response = api_client.get_status()
        
        # Assert response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Parse and validate response data
        data = response.json()
        assert validator.validate_status_response(data)
        
        # Check specific values
        assert data['success'] == True
        assert data['data']['status'] == 'up'
        assert 'appVersion' in data['data']
        
        print(f"✅ API Status: {data['data']['status']}")
        print(f"✅ App Version: {data['data']['appVersion']}")
    
    def test_api_content_endpoint(self, api_client, validator):
        """Test the public content endpoint"""
        print("Testing API content endpoint...")
        
        response = api_client.get_content()
        
        # Assert response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Parse and validate response data
        data = response.json()
        assert validator.validate_content_response(data)
        
        # Check content structure
        content_data = data['data']
        assert isinstance(content_data['backgrounds'], dict)
        assert isinstance(content_data['achievements'], dict)
        assert isinstance(content_data['classes'], list)
        
        print(f"✅ Backgrounds: {len(content_data['backgrounds'])} items")
        print(f"✅ Achievements: {len(content_data['achievements'])} items")
        print(f"✅ Classes: {len(content_data['classes'])} items")
    
    def test_api_world_state_endpoint(self, api_client):
        """Test the public world state endpoint"""
        print("Testing API world state endpoint...")
        
        response = api_client.get_world_state()
        
        # Assert response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        
        # Validate structure
        assert 'success' in data
        assert 'data' in data
        assert data['success'] == True
        
        world_data = data['data']
        assert 'worldDrops' in world_data
        assert 'npc' in world_data
        
        print("✅ World State: Endpoint responding with valid data")
    
    def test_api_response_time(self, api_client):
        """Test API response time performance"""
        print("Testing API response time...")
        
        start_time = time.time()
        response = api_client.get_status()
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 5.0, f"Response time too slow: {response_time:.2f}s"
        
        print(f"✅ Response Time: {response_time:.2f} seconds")
    
    def test_api_error_handling(self):
        """Test API error handling for non-existent endpoints"""
        print("Testing API error handling...")
        
        # Test non-existent endpoint
        response = requests.get(f"{config.API_BASE_URL}/nonexistent-endpoint")
        
        # Should return 404 or proper error
        assert response.status_code in [404, 400, 401]
        
        print("✅ Error Handling: Proper response for invalid endpoints")

def test_api_endpoint_discovery():
    """Test to discover available public endpoints"""
    endpoints = config.PUBLIC_ENDPOINTS
    
    for endpoint in endpoints:
        url = f"{config.API_BASE_URL}{endpoint}"
        print(f"Testing endpoint: {endpoint}")
        
        try:
            response = requests.get(url, timeout=10)
            assert response.status_code == 200
            print(f"✅ {endpoint}: Working")
        except Exception as e:
            print(f"❌ {endpoint}: Failed - {e}")