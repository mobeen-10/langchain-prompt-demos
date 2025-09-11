from helpers import (get_llm, get_response)

llm = get_llm("openai/gpt-4.1-nano")


def demo_garbage_in_garbage_out():
    
    # Bad prompt example
    bad_prompt = "Explain blockchain"
    print(f"Bad Prompt: '{bad_prompt}'")
    get_response(llm, bad_prompt)
    
    # Good prompt example
    good_prompt = """Explain blockchain in 3 bullet points, simple language, as if teaching a junior developer."""
    print(f"\nGood Prompt: '{good_prompt}'")
    get_response(llm, good_prompt)
    


if __name__ == "__main__":
    demo_garbage_in_garbage_out()
