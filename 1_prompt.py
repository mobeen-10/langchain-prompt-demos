from helpers import (get_llm, get_response)

llm = get_llm()

def good_bad_prompt():
    
    # Bad prompt example. not knowing its audience and how much long answer should it be i.e no specificity
    bad_prompt = "blockchain?"
    # Good prompt example
    good_prompt = """Explain blockchain in 3 bullet points, using simple language, as if teaching a junior developer who has never heard of it before."""

    print("="*60)
    print(f"BAD PROMPT: '{bad_prompt}'")
    print("="*60)
    print("BAD PROMPT RESULT:")
    get_response(llm, bad_prompt)
    
    print("="*60)
    print(f"GOOD PROMPT: '{good_prompt}'")
    print("="*60)
    print("GOOD PROMPT RESULT:")
    get_response(llm, good_prompt)
    


if __name__ == "__main__":
    good_bad_prompt()
