import requests
import pytest
from tests.config import config

class HabiticaAPI:
    def __init__(self):
        self.base_url = config.API_BASE_URL
    
    def get_status(self):
        """Check if public API is available"""
        response = requests.get(f"{self.base_url}/status")
        return response
    
    def get_content(self):
        """Get public content (game data, items, etc.)"""
        response = requests.get(f"{self.base_url}/content")
        return response
    
    def get_world_state(self):
        """Get public world state information"""
        response = requests.get(f"{self.base_url}/world-state")
        return response

class TestDataValidator:
    """Utility class to validate API response structures"""
    
    @staticmethod
    def validate_status_response(data):
        """Validate the structure of status endpoint response"""
        assert 'success' in data
        assert 'data' in data
        assert 'status' in data['data']
        return True
    
    @staticmethod
    def validate_content_response(data):
        """Validate the structure of content endpoint response"""
        assert 'success' in data
        assert 'data' in data
        # Check for some expected content keys
        assert 'backgrounds' in data['data']
        assert 'achievements' in data['data']
        return True