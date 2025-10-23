"""Understanding Agent Executor - Clean Code Examples"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from helpers import get_llm


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely"""
    try:
        allowed_chars = set('0123456789+-*/(). ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"Result: {result}"
        else:
            return "Error: Invalid characters in expression"
    except Exception as e:
        return f"Error: {str(e)}"


calculator_tool = Tool(
    name="calculator",
    func=calculate,
    description="Evaluates a mathematical expression. Input should be a valid expression like '2 + 2' or '10 * 5'"
)


def create_simple_agent():
    """Create a simple agent with AgentExecutor"""
    llm = get_llm()
    tools = [calculator_tool]
    
    prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
    
    return agent_executor


def example_basic_usage():
    """Demonstrate basic AgentExecutor usage"""
    print("Example 1: Basic AgentExecutor Usage")
    print("=" * 50)
    
    agent_executor = create_simple_agent()
    
    result = agent_executor.invoke({
        "input": "What is 15 multiplied by 8?"
    })
    
    print(f"\nFinal Result: {result['output']}")


def example_verbose_mode():
    """Demonstrate verbose mode to see agent's thinking"""
    print("\nExample 2: Verbose Mode - See Agent's Thinking")
    print("=" * 50)
    print("Running agent with verbose=True...")
    print("You'll see the agent's reasoning process:\n")
    
    agent_executor = create_simple_agent()
    
    result = agent_executor.invoke({
        "input": "What is 25 + 17, then multiply that by 3?"
    })


def example_max_iterations():
    """Demonstrate max_iterations parameter"""
    print("\nExample 3: Max Iterations")
    print("=" * 50)
    
    llm = get_llm()
    tools = [calculator_tool]
    
    prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=2,  # Will stop after 2 tool calls
    )
    
    print("Running with max_iterations=2...")
    print("This will stop after 2 tool calls even if not done.\n")
    
    result = agent_executor.invoke({
        "input": "What is 10 + 5, then multiply by 2, then add 3?"
    })


def example_error_handling():
    """Demonstrate error handling"""
    print("\nExample 4: Error Handling")
    print("=" * 50)
    
    agent_executor = create_simple_agent()
    
    print("Running agent with an invalid query...")
    print("(This should be handled gracefully)\n")
    
    try:
        result = agent_executor.invoke({
            "input": "This is not a math question at all!"
        })
        print(f"Result: {result['output']}")
    except Exception as e:
        print(f"Error handled: {type(e).__name__}")


def main():
    """Run all examples"""
    print("UNDERSTANDING AGENT EXECUTOR")
    print("=" * 50)
    
    example_basic_usage()
    example_verbose_mode()
    example_max_iterations()
    example_error_handling()
    
    print("\nSee docs/agent_executor.md for detailed explanations")


if __name__ == "__main__":
    main()