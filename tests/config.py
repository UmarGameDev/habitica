import os

class TestConfig:
    # Use the public Habitica API
    BASE_URL = "https://habitica.com"
    API_VERSION = "v3"
    
    @property
    def API_BASE_URL(self):
        return f"{self.BASE_URL}/api/{self.API_VERSION}"
    
    # We'll use public endpoints that don't require authentication
    PUBLIC_ENDPOINTS = [
        "/content",
        "/status",
        "/world-state"
    ]

config = TestConfig()