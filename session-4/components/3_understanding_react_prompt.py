"""Understanding the ReAct Prompt - Clean Code Examples"""

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from helpers import get_llm
from react_prompt import get_react_prompt


def show_react_prompt_anatomy():
    """Show the anatomy of the ReAct prompt"""
    print("ANATOMY OF THE REACT PROMPT")
    
    base_prompt = get_react_prompt()
    template = base_prompt.template
    
    print("ReAct prompt has 5 key sections:")
    print("1. System Instructions - tells agent what to do")
    print("2. Tools Section - {tools} gets replaced with tool descriptions")
    print("3. Format Section - defines Thought/Action/Observation structure")
    print("4. Question Section - {input} contains user's query")
    print("5. Scratchpad Section - {agent_scratchpad} contains reasoning history")
    
    print("\nOur base prompt template:")
    print("-" * 40)
    print(template)
    print("-" * 40)


def show_tool_injection():
    """Show how tool descriptions are injected into the prompt"""
    print("\nHOW TOOL DESCRIPTIONS ARE INJECTED")
    
    print("LangChain automatically:")
    print("1. Takes all tools in the tools list")
    print("2. Extracts name and description from each tool")
    print("3. Formats them in a consistent way")
    print("4. Replaces {tools} in the prompt template")
    
    # Example tools
    tools = [
        Tool(
            name="calculator",
            func=lambda x: f"Result: {eval(x)}",
            description="Evaluates mathematical expressions"
        ),
        Tool(
            name="search",
            func=lambda x: f"Search results for: {x}",
            description="Searches for information"
        )
    ]
    
    print(f"\nExample tools: {[tool.name for tool in tools]}")
    print("These get formatted and injected into the prompt")


def show_prompt_variations():
    """Show different prompt variations"""
    print("\nPROMPT VARIATIONS")
    
    # Base prompt
    base_prompt = get_react_prompt()
    print("1. Base Prompt (verbose):")
    print(f"   Length: {len(base_prompt.template)} characters")
    
    # Concise prompt
    concise_prompt = get_react_prompt(concise=True)
    print("2. Concise Prompt:")
    print(f"   Length: {len(concise_prompt.template)} characters")
    
    # Custom prompt
    custom_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use these tools:

{tools}

Format:
Question: {input}
Thought: {agent_scratchpad}
""")
    print("3. Custom Prompt:")
    print(f"   Length: {len(custom_prompt.template)} characters")


def show_langchain_hub_prompt():
    """Show how to use LangChain Hub prompts"""
    print("\nLANGCHAIN HUB PROMPTS")
    
    try:
        # Try to get the official ReAct prompt from LangChain Hub
        hub_prompt = hub.pull("hwchase17/react")
        print("Official ReAct prompt from LangChain Hub:")
        print(f"   Length: {len(hub_prompt.template)} characters")
        print("   This is the standard ReAct prompt used by the community")
    except Exception as e:
        print(f"Could not load from LangChain Hub: {e}")
        print("This is normal if you don't have internet access")


def create_agent_with_custom_prompt():
    """Create an agent with a custom prompt"""
    print("\nCUSTOM PROMPT EXAMPLE")
    
    llm = get_llm()
    
    # Custom prompt
    custom_prompt = PromptTemplate.from_template("""
You are a math assistant. Use the calculator tool when needed.

Tools: {tools}

Question: {input}
Thought: {agent_scratchpad}
""")
    
    # Simple calculator tool
    def calculate(expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    tools = [
        Tool(
            name="calculator",
            func=calculate,
            description="Evaluates mathematical expressions"
        )
    ]
    
    agent = create_react_agent(llm, tools, custom_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )
    
    print("Testing custom prompt...")
    result = agent_executor.invoke({
        "input": "What is 15 * 8?"
    })
    
    print(f"Result: {result['output']}")


def main():
    """Run all examples"""
    print("UNDERSTANDING REACT PROMPTS")
    print("=" * 50)
    
    show_react_prompt_anatomy()
    show_tool_injection()
    show_prompt_variations()
    show_langchain_hub_prompt()
    create_agent_with_custom_prompt()
    
    print("\nSee docs/react_pattern.md for detailed explanations")


if __name__ == "__main__":
    main()