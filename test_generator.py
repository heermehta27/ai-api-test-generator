import os
import json
from google import genai
from prompt_template import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

def generate_test_cases(api_endpoint: str, method: str, request_body: dict) -> list[dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Environment variable 'GEMINI_API_KEY' is not set.")
        
    client = genai.Client(api_key=api_key)
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        api_endpoint=api_endpoint,
        method=method.upper(),
        request_body=json.dumps(request_body, indent=2)
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        
        content = response.text.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
            
        return json.loads(content.strip())
        
    except json.JSONDecodeError as err:
        raise Exception(f"Failed to parse LLM response into JSON. Raw response: {content}") from err
    except Exception as err:
        raise Exception(f"An error occurred while calling the LLM API: {str(err)}") from err
