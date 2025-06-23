#!/usr/bin/env python3
"""
Backend testing script - Tests various scenarios including error cases
"""

import sys

import requests

# Configuration
BASE_URL = "http://localhost:8000"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result with color"""
    status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
    print(f"[{status}] {name}")
    if details:
        print(f"      {YELLOW}{details}{RESET}")


def test_health_endpoint():
    """Test the health check endpoint"""
    print(f"\n{BLUE}Testing Health Endpoint...{RESET}")

    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()

        print_test("Health endpoint accessible", response.status_code == 200)
        print_test("Redis status returned", "redis" in data)
        print_test("Claude status returned", "claude" in data)

        print(f"      Redis: {data.get('redis', 'unknown')}")
        print(f"      Claude: {data.get('claude', 'unknown')}")

        return response.status_code == 200
    except Exception as e:
        print_test("Health endpoint", False, str(e))
        return False


def test_analyze_endpoint():
    """Test the analyze endpoint with various inputs"""
    print(f"\n{BLUE}Testing Analyze Endpoint...{RESET}")

    test_cases = [
        {
            "name": "Valid prompt",
            "data": {"prompt": "Tell me about Python programming"},
            "expect_success": True,
        },
        {"name": "Empty prompt", "data": {"prompt": ""}, "expect_success": False},
        {
            "name": "Very long prompt",
            "data": {"prompt": "x" * 2001},
            "expect_success": False,
        },
        {"name": "Missing prompt field", "data": {}, "expect_success": False},
        {
            "name": "Special characters",
            "data": {"prompt": "Explain this: 🚀 && || <script>alert('test')</script>"},
            "expect_success": True,
        },
    ]

    all_passed = True

    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/analyze",
                json=test["data"],
                headers={"Content-Type": "application/json"},
            )

            success = (response.status_code == 200) == test["expect_success"]

            if response.status_code == 200:
                data = response.json()
                details = f"Score: {data.get('score', 'N/A')}/10"
            else:
                details = (
                    f"Status: {response.status_code}, Error: {response.text[:100]}"
                )

            print_test(test["name"], success, details)

            if not success:
                all_passed = False

        except Exception as e:
            print_test(test["name"], False, str(e))
            all_passed = False

    return all_passed


def test_examples_endpoint():
    """Test the examples endpoint"""
    print(f"\n{BLUE}Testing Examples Endpoint...{RESET}")

    try:
        response = requests.get(f"{BASE_URL}/examples")
        data = response.json()

        print_test("Examples endpoint accessible", response.status_code == 200)
        print_test(
            "Examples returned", "examples" in data and len(data["examples"]) > 0
        )

        if "examples" in data:
            print(f"      Found {len(data['examples'])} examples")

        return response.status_code == 200
    except Exception as e:
        print_test("Examples endpoint", False, str(e))
        return False


def test_cors_headers():
    """Test CORS configuration"""
    print(f"\n{BLUE}Testing CORS Headers...{RESET}")

    try:
        response = requests.options(
            f"{BASE_URL}/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        cors_headers_present = "access-control-allow-origin" in response.headers
        print_test("CORS headers present", cors_headers_present)

        if cors_headers_present:
            print(
                f"      Allow-Origin: {response.headers.get('access-control-allow-origin')}"
            )

        return cors_headers_present
    except Exception as e:
        print_test("CORS configuration", False, str(e))
        return False


def main():
    """Run all tests"""
    print(f"{BLUE}{'=' * 50}{RESET}")
    print(f"{BLUE}Prompt Analyzer Backend Test Suite{RESET}")
    print(f"{BLUE}{'=' * 50}{RESET}")

    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except Exception:
        print(f"\n{RED}ERROR: Backend server is not running!{RESET}")
        print(f"Please start it with: {YELLOW}uvicorn main:app --reload{RESET}")
        sys.exit(1)

    # Run tests
    results = [
        test_health_endpoint(),
        test_analyze_endpoint(),
        test_examples_endpoint(),
        test_cors_headers(),
    ]

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\n{BLUE}{'=' * 50}{RESET}")
    print(f"Summary: {passed}/{total} test suites passed")

    if passed == total:
        print(f"{GREEN}All tests passed!{RESET}")
    else:
        print(f"{RED}Some tests failed. Check the logs above.{RESET}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
