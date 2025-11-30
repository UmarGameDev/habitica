import requests
import json
import time
from datetime import datetime

def generate_habitica_api_test_report():
    """Generate a comprehensive test report for Habitica API endpoints"""
    
    BASE_URL = "https://habitica.com/api/v3"
    
    # Test endpoints with their expected behavior
    test_cases = [
        {
            "name": "API Status",
            "endpoint": "/status",
            "method": "GET",
            "auth_required": False,
            "expected_status": 200
        },
        {
            "name": "World State", 
            "endpoint": "/world-state",
            "method": "GET",
            "auth_required": False,
            "expected_status": 200
        },
        {
            "name": "Content (Protected)",
            "endpoint": "/content",
            "method": "GET", 
            "auth_required": True,
            "expected_status": 401,
            "params": {"language": "en"}
        },
        {
            "name": "User Profile (Protected)",
            "endpoint": "/user",
            "method": "GET",
            "auth_required": True, 
            "expected_status": 401
        },
        {
            "name": "Invalid Endpoint",
            "endpoint": "/invalid-endpoint-12345",
            "method": "GET",
            "auth_required": False,
            "expected_status": 404
        }
    ]
    
    print("=" * 70)
    print("HABITICA API COMPREHENSIVE TEST REPORT")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print("=" * 70)
    
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "response_times": []
    }
    
    # Test headers for authenticated endpoints
    test_headers = {
        'x-client': 'api-test-report',
        'x-api-user': 'test-user',
        'x-api-key': 'test-key'
    }
    
    for test_case in test_cases:
        results["total_tests"] += 1
        url = BASE_URL + test_case["endpoint"]
        
        print(f"\n📊 Test: {test_case['name']}")
        print(f"   Endpoint: {test_case['method']} {test_case['endpoint']}")
        print(f"   Auth Required: {'Yes' if test_case['auth_required'] else 'No'}")
        print(f"   Expected: HTTP {test_case['expected_status']}")
        
        try:
            # Prepare request parameters
            headers = test_headers if test_case["auth_required"] else {}
            params = test_case.get("params", {})
            
            # Measure response time
            start_time = time.time()
            
            if test_case["method"] == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            else:
                response = requests.post(url, headers=headers, json=params, timeout=10)
            
            end_time = time.time()
            response_time = end_time - start_time
            results["response_times"].append(response_time)
            
            # Analyze response
            status_emoji = "✅" if response.status_code == test_case["expected_status"] else "❌"
            
            print(f"   {status_emoji} Actual: HTTP {response.status_code}")
            print(f"   ⏱️  Response Time: {response_time:.2f}s")
            
            if response.status_code == test_case["expected_status"]:
                results["passed"] += 1
                
                # Additional analysis for successful responses
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('success'):
                            print(f"   📈 Success: True")
                            if 'data' in data:
                                data_keys = list(data['data'].keys())[:5]  # Show first 5 keys
                                print(f"   🔑 Data Keys: {data_keys}")
                        if 'appVersion' in data:
                            print(f"   🏷️  App Version: {data['appVersion']}")
                    except json.JSONDecodeError:
                        print(f"   ⚠️  Response: Non-JSON content")
                
                # Analysis for error responses
                elif response.status_code >= 400:
                    try:
                        error_data = response.json()
                        print(f"   🚫 Error Type: {error_data.get('error', 'Unknown')}")
                        print(f"   💬 Message: {error_data.get('message', 'No message')}")
                    except json.JSONDecodeError:
                        print(f"   🚫 Error: Non-JSON error response")
            
            else:
                results["failed"] += 1
                print(f"   ❌ FAILED: Expected {test_case['expected_status']}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   💬 Response: {error_data}")
                except:
                    print(f"   💬 Response: {response.text[:100]}...")
        
        except requests.exceptions.Timeout:
            results["failed"] += 1
            print(f"   ❌ TIMEOUT: Request took longer than 10 seconds")
        
        except requests.exceptions.ConnectionError:
            results["failed"] += 1
            print(f"   ❌ CONNECTION ERROR: Could not connect to API")
        
        except Exception as e:
            results["failed"] += 1
            print(f"   ❌ EXCEPTION: {str(e)}")
    
    # Generate summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    # Calculate statistics
    pass_rate = (results["passed"] / results["total_tests"]) * 100 if results["total_tests"] > 0 else 0
    avg_response_time = sum(results["response_times"]) / len(results["response_times"]) if results["response_times"] else 0
    max_response_time = max(results["response_times"]) if results["response_times"] else 0
    min_response_time = min(results["response_times"]) if results["response_times"] else 0
    
    print(f"📈 Total Tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"📊 Pass Rate: {pass_rate:.1f}%")
    print(f"\n⏱️  Performance Metrics:")
    print(f"   Average Response Time: {avg_response_time:.2f}s")
    print(f"   Fastest Response: {min_response_time:.2f}s")
    print(f"   Slowest Response: {max_response_time:.2f}s")
    
    # Performance assessment
    if avg_response_time < 1.0:
        performance_rating = "Excellent 🚀"
    elif avg_response_time < 2.0:
        performance_rating = "Good 👍"
    elif avg_response_time < 3.0:
        performance_rating = "Acceptable ⚡"
    else:
        performance_rating = "Needs Improvement 🐢"
    
    print(f"   Overall Performance: {performance_rating}")
    
    # API Health Assessment
    if pass_rate >= 90:
        health_status = "Healthy 💚"
    elif pass_rate >= 70:
        health_status = "Moderate 💛"
    else:
        health_status = "Unhealthy ❤️"
    
    print(f"\n🏥 API Health Status: {health_status}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if results["failed"] > 0:
        print(f"   - Investigate failed test cases")
    if max_response_time > 3.0:
        print(f"   - Monitor slow endpoints for performance issues")
    if pass_rate < 100:
        print(f"   - Review authentication requirements for protected endpoints")
    
    print("=" * 70)

def test_specific_endpoint_details():
    """Test specific endpoint details and data structures"""
    print("\n" + "=" * 70)
    print("ENDPOINT DETAIL ANALYSIS")
    print("=" * 70)
    
    BASE_URL = "https://habitica.com/api/v3"
    
    # Test status endpoint in detail
    print("\n🔍 Detailed Analysis: /status endpoint")
    response = requests.get(f"{BASE_URL}/status")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['data']['status']}")
        print(f"📋 Response Structure:")
        print(f"   - success: {data['success']} (boolean)")
        print(f"   - data: object with {len(data['data'])} properties")
        
        for key, value in data['data'].items():
            value_type = type(value).__name__
            print(f"     • {key}: {value} ({value_type})")
        
        # Check for additional top-level fields
        additional_fields = [key for key in data.keys() if key not in ['success', 'data']]
        if additional_fields:
            print(f"   - Additional fields: {additional_fields}")
    
    # Test world-state endpoint in detail
    print("\n🔍 Detailed Analysis: /world-state endpoint")
    response = requests.get(f"{BASE_URL}/world-state")
    
    if response.status_code == 200:
        data = response.json()
        world_data = data['data']
        print(f"📋 World State Structure:")
        print(f"   - success: {data['success']}")
        print(f"   - data: object with {len(world_data)} properties")
        
        for key, value in world_data.items():
            value_type = type(value).__name__
            if isinstance(value, (list, dict)):
                print(f"     • {key}: {value_type} with {len(value)} items")
            else:
                print(f"     • {key}: {value} ({value_type})")

def generate_ci_test_report():
    """Generate test report formatted for CI/CD pipelines"""
    print("::group::📊 Backend Test Summary")
    generate_habitica_api_test_report()
    print("::endgroup::")

def generate_junit_style_report():
    """Generate machine-readable test results for CI"""
    BASE_URL = "https://habitica.com/api/v3"
    
    test_cases = [
        {"name": "API Status", "endpoint": "/status", "expected": 200},
        {"name": "World State", "endpoint": "/world-state", "expected": 200},
        {"name": "Invalid Endpoint", "endpoint": "/invalid-endpoint", "expected": 404},
    ]
    
    results = []
    
    for test_case in test_cases:
        url = BASE_URL + test_case["endpoint"]
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            passed = response.status_code == test_case["expected"]
            
            results.append({
                "name": test_case["name"],
                "passed": passed,
                "time": response_time,
                "status": response.status_code
            })
            
            # CI-friendly output
            if passed:
                print(f"✅ PASS: {test_case['name']} ({response_time:.2f}s)")
            else:
                print(f"❌ FAIL: {test_case['name']} - Expected {test_case['expected']}, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {test_case['name']} - {str(e)}")
            results.append({
                "name": test_case["name"],
                "passed": False,
                "time": 0,
                "status": "ERROR"
            })
    
    # Summary for CI
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    
    print(f"Tests Passed: {passed_count}/{total_count}")
    print(f"Pass Rate: {passed_count/total_count*100:.1f}%")

# Update the main block to support CI mode
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--ci":
        generate_ci_test_report()
        generate_junit_style_report()
    else:
        generate_habitica_api_test_report()
        test_specific_endpoint_details()