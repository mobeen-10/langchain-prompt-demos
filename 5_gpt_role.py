#!/usr/bin/env python3

from helpers import get_llm, get_response

gpt_5 = "openai/gpt-5-nano"
gpt_5_mini="openai/gpt-5-mini"
gpt_4 = "openai/gpt-4.1-nano"

def which_model():
    prompt = "Which model are you? Please tell me your model name and any relevant details about yourself."
    try:
        get_response(get_llm(gpt_4), prompt)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    which_model()
