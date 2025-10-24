from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from helpers import get_llm
from react_prompt import get_react_prompt


def calculator(expression: str) -> str:
    """Simple calculator"""
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
        func=calculator,
        description="Evaluates a mathematical expression. Input should be like '2 + 2' or '10 * 5'"
    ),
    Tool(
        name="search",
        func=search_knowledge_base,
        description="Searches a knowledge base for information about topics like Python, LangChain, or agents"
    )
]


def create_react_agent_demo():
    """Create a ReAct agent for demonstration"""
    llm = get_llm(model_name="openai/gpt-4o", temperature=0.0)
    prompt = get_react_prompt()
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )
    
    return agent_executor


def example_simple_math():
    
    agent = create_react_agent_demo()
    result = agent.invoke({
        "input": "What is 15 * 8?"
    })
    
    print(f"Final Answer: {result['output']}")


def example_multi_step():
    
    agent = create_react_agent_demo()
    result = agent.invoke({
        "input": "What is 20 + 10, then subtract 5, then multiply by 2?"
    })
    
    print(f"Final Answer: {result['output']}")


def example_information_retrieval():
    
    agent = create_react_agent_demo()
    result = agent.invoke({
        "input": "What is Python?"
    })
    
    print(f"Final Answer: {result['output']}")


def example_mixed_tools():
    
    agent = create_react_agent_demo()
    result = agent.invoke({
        "input": "What is LangChain, and what is 10 * 5?"
    })
    
    print(f"Final Answer: {result['output']}")

def main():
    example_simple_math()
    example_multi_step()
    example_information_retrieval()
    example_mixed_tools()



if __name__ == "__main__":
    main()