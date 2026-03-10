import os
import json
import pytest
from playwright.sync_api import APIRequestContext
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

test_suite_path = "generated_test_suite.json"
test_cases = []
if os.path.exists(test_suite_path):
    with open(test_suite_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

def generate_ids():
    return [f"{tc.get('category').upper()} - {tc.get('test_case_id')}" for tc in test_cases]

@pytest.fixture(scope="session")
def base_url():
    return API_BASE_URL

@pytest.mark.parametrize("test_case", test_cases, ids=generate_ids())
def test_dynamic_api_cases(playwright, test_case, base_url):
    api_request_context: APIRequestContext = playwright.request.new_context(base_url=base_url)
    
    scenario = test_case.get("scenario", "Unknown Scenario")
    payload = test_case.get("input", {})
    expected_status = int(test_case.get("expected_status_code", 200))

    endpoint = "/api/v1/users"
    
    print(f"\n[Test Setup] Executing: {scenario}")
    print(f"[Test Execution] POST {base_url}{endpoint} with payload: {json.dumps(payload)}")
    
    try:
        response = api_request_context.post(endpoint, data=payload)
        
        assert response.status == expected_status, \
            f"Expected {expected_status}, but got {response.status}. Response Body: {response.text()}"
            
    finally:
        api_request_context.dispose()
