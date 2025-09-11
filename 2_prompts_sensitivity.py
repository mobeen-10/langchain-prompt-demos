from helpers import (get_llm, get_response)

llm = get_llm()

def demo_sensitivity_to_phrasing():
    
    # Extremely vague prompt - will get useless generic advice
    prompt1 = "python help"
    print(f"Prompt 1: '{prompt1}'")
    get_response(llm, prompt1)
    
    # Specific error but no context - will get some help but not actionable
    prompt2 = "KeyError: 'email' in python"
    print(f"\nPrompt 2: '{prompt2}'")
    get_response(llm, prompt2)
    
    # Highly specific with context and structure
    prompt3 = """I'm debugging a Python function that processes user data from a JSON API. Here's the exact error and context:

ERROR: KeyError: 'email'
File: /app/user_processor.py, line 23, in process_user
    user_email = user_data['email']

CONTEXT:
- Function: process_user(user_data: dict) -> dict
- Input user_data: {"name": "John", "age": 30}
- Expected: Extract email, name, age from user_data
- Current behavior: Crashes when 'email' key is missing

REQUIREMENTS:
1. Why is it crashing?
2. Handle missing keys gracefully
3. Provide fallback values
4. Log warnings for missing data
5. Return processed user dict

Please provide a complete solution with error handling."""
    print(f"\nPrompt 3: '{prompt3}'")
    get_response(llm, prompt3)


if __name__ == "__main__":
    demo_sensitivity_to_phrasing()
