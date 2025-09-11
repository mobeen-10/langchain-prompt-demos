#!/usr/bin/env python3

from helpers import get_llm, get_response

gpt_5 = "openai/gpt-5-nano"
gpt_5_mini="openai/gpt-5-mini"
gpt_4 = "openai/gpt-4.1-nano"
gpt_3 = "openai/gpt-3.5-turbo"

def which_model():
    prompt = "Which model are you? Please tell me your model name. Give an anwer: GPT 3, GPT 4 or GPT 5 - no extra info or text. Be Precise, do not hallucinate or make up information."
    try:
        get_response(get_llm(gpt_5), prompt)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    which_model()
