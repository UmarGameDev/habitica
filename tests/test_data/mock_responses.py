# Mock data for testing various scenarios
MOCK_STATUS_RESPONSE = {
    "success": True,
    "data": {
        "status": "up"
    },
    "appVersion": "5.42.0"
}

MOCK_WORLD_STATE_RESPONSE = {
    "success": True,
    "data": {
        "currentEvent": {
            "start": "2025-11-20T09:00:00.000Z",
            "end": "2025-12-01T08:59:00.000Z",
            "season": "thanksgiving"
        },
        "worldBoss": {},
        "npcImageSuffix": "_thanksgiving"
    }
}

MOCK_ERROR_RESPONSE = {
    "success": False,
    "error": "BadRequest",
    "message": "Missing required parameters"
}

MOCK_USER_DATA = {
    "id": "mock-user-123",
    "username": "testuser",
    "profile": {"name": "Test User"},
    "stats": {"hp": 50, "mp": 30, "exp": 100}
}

MOCK_TASK_DATA = {
    "id": "task-123",
    "type": "habit",
    "text": "Exercise daily",
    "value": 0,
    "priority": 1.5,
    "completed": False
}

# Test scenarios
SCENARIOS = {
    "success": MOCK_STATUS_RESPONSE,
    "error": MOCK_ERROR_RESPONSE,
    "user_data": MOCK_USER_DATA,
    "task_data": MOCK_TASK_DATA
}