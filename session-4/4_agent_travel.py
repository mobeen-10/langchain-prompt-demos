from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from helpers import get_llm
from tools import get_travel_tools


def create_travel_agent():
    """Create a ReAct travel agent using the official LangChain Hub prompt."""
    # Get the LLM (strong model, deterministic)
    llm = get_llm(model_name="openai/gpt-4o", temperature=0.0)
    
    # Get all travel tools
    tools = get_travel_tools()
    
    # Use the official ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Wrap in AgentExecutor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=12,
        handle_parsing_errors=True,
    )
    
    return agent_executor


# ============================================================================
# Example 1: Simple Query
# ============================================================================

def example_1_simple_query():
    agent = create_travel_agent()
    result = agent.invoke({
        "input": "What's the weather in Naran?"
    })
    
    print("Done: used only the needed tool.")


# ============================================================================
# Example 2: Complex Query
# ============================================================================

def example_2_complex_query():
    agent = create_travel_agent()
    result = agent.invoke({
        "input": "Plan a weekend trip for me. I have 3 days and want to travel up to 500km by road. I prefer cloudy weather."
    })
    


# ============================================================================
# Example 3: Budget-Centric Query
# ============================================================================

def example_3_budget_query():    
    agent = create_travel_agent()
    result = agent.invoke({
        "input": "Plan a short iterinary for 3-day trip to Naran with a 400 rupees budget including visiting spots in bullet points"
    })
    
    print("Done: focused on budget only.")


# ============================================================================
# Example 4: Multi-Step Query
# ============================================================================

def example_4_multi_step_query():
    agent = create_travel_agent()
    result = agent.invoke({
        "input": "What's the distance from Lahore to Murree, and how long would it take to drive there?"
    })
    
    print("Done: multi-step handled.")


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run examples"""
    print("TRAVEL AGENT PLANNER")
    
    # Run examples
    # example_1_simple_query()
    # print("\n\n")
    
    # example_2_complex_query()
    # print("\n\n")
    
    # example_3_budget_query()
    # print("\n\n")
    
    example_4_multi_step_query()



if __name__ == "__main__":
    main()

