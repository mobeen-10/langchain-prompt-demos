from helpers import (get_llm, get_response, get_response_with_system)

# Initialize the LLM
llm = get_llm()

def demo_shot_prompting():

    task = "Classify the sentiment of this text: 'I absolutely love this new restaurant!'"

    zero_shot_prompt = f"Task: {task}"
    get_response(llm, zero_shot_prompt)
    

    one_shot_prompt = f"""
    Task: Classify text sentiment as Positive, Negative, or Neutral.
    
    Example:
    Text: "This movie was terrible and boring."
    Sentiment: Negative
    
    Now classify:
    Text: "I absolutely love this new restaurant!"
    Sentiment:
    """
    get_response(llm, one_shot_prompt)
    

    few_shot_prompt = f"""
    Task: Classify text sentiment as Positive, Negative, or Neutral.
    
    Examples:
    Text: "This movie was terrible and boring."
    Sentiment: Negative
    
    Text: "The weather is okay today."
    Sentiment: Neutral
    
    Text: "I'm thrilled with my new car!"
    Sentiment: Positive
    
    Text: "The service was disappointing."
    Sentiment: Negative
    
    Now classify:
    Text: "I absolutely love this new restaurant!"
    Sentiment:
    """

    get_response(llm, few_shot_prompt)


def demo_chain_of_thought():
    tricky_problem = "Count how many times the letter 'r' appears in the word 'strawberries'."
    test_llm = get_llm()
    
    # Without Chain-of-Thought
    print("🔸 WITHOUT Chain-of-Thought (Direct Answer)")
    direct_prompt = f"{tricky_problem}"
    get_response(test_llm, direct_prompt)
    
    # With Chain-of-Thought
    print("\n🔸 WITH Chain-of-Thought (Step-by-Step)")

    cot_prompt = f"""
Solve this problem step by step, showing your reasoning:

Problem: {tricky_problem}

Let's work through this systematically:
1. Write out the word: "strawberries"
2. Go through each letter one by one
3. Count how many times you see the letter 'r'
4. Show your work as you go
5. Give the final count

Step-by-step solution:
"""
    get_response(test_llm, cot_prompt)


def demo_role_based_prompting():
    
    topic = "the impact of remote work on team productivity"
    

    generic_prompt = f"Write about {topic}."
    get_response(llm, generic_prompt)
    
    # WITH ROLE - HR Director
    hr_system = "You are an experienced HR Director with 12 years of experience in employee engagement, organizational culture, and talent retention. You focus on people-first approaches and employee wellbeing."
    hr_user = f"Analyze {topic}, focusing on employee engagement, team culture, work-life balance, and retention strategies."
    print(f"System: '{hr_system}'")
    print(f"User: '{hr_user}'")
    get_response_with_system(llm, hr_system, hr_user)
    print("\n" + "-"*60)
    # WITH ROLE - TPM
    tpm_system = "You are an experienced Technical Program Manager with 8 years of experience in cross-functional coordination, project delivery, and process optimization. You focus on timeline management, stakeholder alignment, and delivery excellence."
    tpm_user = f"Analyze {topic}, focusing on project delivery, cross-team collaboration, process efficiency, and timeline management."
    print(f"System: '{tpm_system}'")
    print(f"User: '{tpm_user}'")
    get_response_with_system(llm, tpm_system, tpm_user)
    

def run_strategies_demo():
    try:
        demo_shot_prompting()
        print("\n" + "-"*60)
        demo_chain_of_thought()
        print("\n" + "-"*60)
        demo_role_based_prompting()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    run_strategies_demo()
