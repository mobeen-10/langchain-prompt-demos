"""Understanding Agent Scratchpad - Clean Code Examples"""

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
            return f"{result}"
        else:
            return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"


def search_knowledge_base(query: str) -> str:
    """Simple knowledge base search"""
    knowledge = {
        "python": "Python is a high-level programming language.",
        "langchain": "LangChain is a framework for building LLM applications.",
        "agents": "Agents are systems that can use tools to accomplish tasks.",
    }
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    return "No information found."


tools = [
    Tool(
        name="calculator",
        func=calculate,
        description="Evaluates a mathematical expression. Input should be like '2 + 2' or '10 * 5'"
    ),
    Tool(
        name="search",
        func=search_knowledge_base,
        description="Searches a knowledge base for information about topics like Python, LangChain, or agents"
    )
]


def create_agent_with_scratchpad():
    """Create an agent that demonstrates scratchpad usage"""
    llm = get_llm()
    
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
        max_iterations=10,
        handle_parsing_errors=True,
    )
    
    return agent_executor


def example_simple_math():
    """Simple math problem showing scratchpad evolution"""
    print("Example 1: Simple Math Problem")
    print("Query: 'What is 15 * 8?'")
    print("Watch the scratchpad build up step by step:\n")
    
    agent = create_agent_with_scratchpad()
    result = agent.invoke({
        "input": "What is 15 * 8?"
    })
    
    print(f"\nFinal Answer: {result['output']}")


def example_multi_step():
    """Multi-step problem showing scratchpad evolution"""
    print("\nExample 2: Multi-Step Problem")
    print("Query: 'What is 20 + 10, then subtract 5, then multiply by 2?'")
    print("Watch the scratchpad build up over multiple steps:\n")
    
    agent = create_agent_with_scratchpad()
    result = agent.invoke({
        "input": "What is 20 + 10, then subtract 5, then multiply by 2?"
    })
    
    print(f"\nFinal Answer: {result['output']}")


def example_mixed_tools():
    """Mixed tool usage showing scratchpad evolution"""
    print("\nExample 3: Mixed Tool Usage")
    print("Query: 'What is Python, and what is 10 * 5?'")
    print("Watch the scratchpad show reasoning for different tools:\n")
    
    agent = create_agent_with_scratchpad()
    result = agent.invoke({
        "input": "What is Python, and what is 10 * 5?"
    })
    
    print(f"\nFinal Answer: {result['output']}")


def show_scratchpad_structure():
    """Show the structure of the scratchpad"""
    print("\nScratchpad Structure:")
    print("=" * 50)
    print("""
The scratchpad follows this pattern:

Thought: [Agent's reasoning about what to do next]
Action: [Tool name to use]
Action Input: [Parameters for the tool]
Observation: [Result from the tool]

Thought: [Agent's reasoning based on the observation]
Action: [Next tool to use, or Final Answer]
Action Input: [Parameters, or empty for Final Answer]
Observation: [Result, or empty for Final Answer]

... continues until Final Answer

Key Points:
- Each Thought builds on previous Observations
- The agent can see its entire reasoning history
- This enables complex multi-step problem solving
- The scratchpad is the agent's working memory
    """)


def main():
    """Run all examples"""
    print("UNDERSTANDING AGENT SCRATCHPAD")
    print("=" * 50)
    
    example_simple_math()
    example_multi_step()
    example_mixed_tools()
    show_scratchpad_structure()
    
    print("\nSee docs/scratchpad.md for detailed explanations")


if __name__ == "__main__":
    main()