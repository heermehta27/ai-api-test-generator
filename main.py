import json
import os
import sys
from dotenv import load_dotenv
from test_generator import generate_test_cases

def main():
    load_dotenv()
    
    sample_input_path = "sample_input.json"
    
    if not os.path.exists(sample_input_path):
        print(f"Error: Required file '{sample_input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(sample_input_path, "r", encoding="utf-8") as f:
        try:
            sample_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing '{sample_input_path}': {e}", file=sys.stderr)
            sys.exit(1)
            
    api_endpoint = "/api/v1/users"
    method = "POST"
    request_body = sample_data
    
    print(f"[*] Analyzing API Target: {method} {api_endpoint}")
    print("[*] Generating comprehensive test suite using AI...")
    
    try:
        test_cases = generate_test_cases(api_endpoint, method, request_body)
        
        print("\n=== GENERATED TEST CASES ===\n")
        print(json.dumps(test_cases, indent=2))
        
        output_file = "generated_test_suite.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(test_cases, f, indent=2)
            
        print(f"\n[*] Execution successful. Saved output to '{output_file}'.")
        
        print("\n[*] Starting Playwright API Test Execution...")
        import pytest
        retcode = pytest.main(["test_runner.py", "-v"])
        sys.exit(retcode)
        
    except ValueError as ve:
        print(f"\n[!] Configuration Error: {ve}", file=sys.stderr)
    except Exception as e:
        print(f"\n[!] System Error: An unexpected error occurred:\n{e}", file=sys.stderr)

if __name__ == "__main__":
    main()
