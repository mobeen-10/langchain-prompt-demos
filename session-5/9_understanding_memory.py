"""
Understanding Agent Memory

This file explains how to add memory to agents for multi-turn conversations.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from helpers import get_llm


# ============================================================================
# What is Agent Memory?
# ============================================================================

"""
Agent memory allows agents to remember previous conversations.

Without memory:
- Each query is independent
- Agent doesn't remember previous context
- Can't handle follow-up questions

With memory:
- Agent remembers conversation history
- Can handle follow-up questions
- Provides context-aware responses
"""


# ============================================================================
# Example: Agent Without Memory
# ============================================================================

def example_without_memory():
    """Show agent without memory"""
    print("=" * 70)
    print("EXAMPLE: AGENT WITHOUT MEMORY")
    print("=" * 70)
    
    # Create tools
    def calculator(expression: str) -> str:
        try:
            allowed_chars = set('0123456789+-*/(). ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"{result}"
            else:
                return "Error: Invalid expression"
        except Exception as e:
            return f"Error: {str(e)}"
    
    tools = [
        Tool(
            name="calculator",
            func=calculator,
            description="Evaluates a mathematical expression"
        )
    ]
    
    # Create agent without memory
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
        max_iterations=5
    )
    
    print("\nQuery 1: What is 10 + 5?")
    result1 = agent_executor.invoke({"input": "What is 10 + 5?"})
    print(f"Answer: {result1['output']}\n")
    
    print("Query 2: Now multiply that by 3")
    print("(Agent doesn't remember previous answer!)\n")
    result2 = agent_executor.invoke({"input": "Now multiply that by 3"})
    print(f"Answer: {result2['output']}")
    
    print("\n" + "=" * 70)
    print("Problem: Agent doesn't remember 'that' refers to 15!")
    print("=" * 70)


# ============================================================================
# Example: Agent With Memory
# ============================================================================

def example_with_memory():
    """Show agent with memory"""
    print("\n" + "=" * 70)
    print("EXAMPLE: AGENT WITH MEMORY")
    print("=" * 70)
    
    # Create tools
    def calculator(expression: str) -> str:
        try:
            allowed_chars = set('0123456789+-*/(). ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"{result}"
            else:
                return "Error: Invalid expression"
        except Exception as e:
            return f"Error: {str(e)}"
    
    tools = [
        Tool(
            name="calculator",
            func=calculator,
            description="Evaluates a mathematical expression"
        )
    ]
    
    # Create memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create agent with memory
    llm = get_llm()
    prompt = PromptTemplate.from_template("""
You are a helpful assistant. You have access to the following tools:

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

Previous conversation:
{chat_history}

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=5
    )
    
    print("\nQuery 1: What is 10 + 5?")
    result1 = agent_executor.invoke({"input": "What is 10 + 5?"})
    print(f"Answer: {result1['output']}\n")
    
    print("Query 2: Now multiply that by 3")
    result2 = agent_executor.invoke({"input": "Now multiply that by 3"})
    print(f"Answer: {result2['output']}")
    
    print("\n" + "=" * 70)
    print("Success: Agent remembers 'that' refers to 15!")
    print("=" * 70)


# ============================================================================
# Types of Memory
# ============================================================================

def explain_memory_types():
    """Explain different types of memory"""
    print("\n" + "=" * 70)
    print("TYPES OF MEMORY")
    print("=" * 70)
    
    print("""
1. ConversationBufferMemory
   - Stores entire conversation history
   - Simple and effective
   - Can grow large over time
   - Best for short conversations

2. ConversationSummaryMemory
   - Summarizes conversation history
   - Keeps memory size manageable
   - Loses some details
   - Best for long conversations

3. ConversationBufferWindowMemory
   - Keeps only recent messages
   - Fixed size memory
   - Forgets old messages
   - Best for focused conversations

4. ConversationSummaryBufferMemory
   - Combines summary and buffer
   - Keeps recent messages + summary
   - Balances detail and size
   - Best for most use cases


Choosing the Right Memory:
--------------------------
- Short conversations: ConversationBufferMemory
- Long conversations: ConversationSummaryMemory
- Focused conversations: ConversationBufferWindowMemory
- General purpose: ConversationSummaryBufferMemory
    """)


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("UNDERSTANDING AGENT MEMORY")
    print("=" * 70)
    
    print("""
Agent memory enables multi-turn conversations.
It's essential for building conversational agents.
    """)
    
    # Run examples
    example_without_memory()
    print("\n\n")
    
    example_with_memory()
    print("\n\n")
    
    explain_memory_types()
    
    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("=" * 70)
    print("""
1. Memory enables multi-turn conversations
2. ConversationBufferMemory is simple and effective
3. Different memory types suit different needs
4. Memory is essential for conversational agents
5. Choose memory type based on use case
    """)
    
    print("\n" + "=" * 70)
    print("Next: Check out 10_error_handling.py")
    print("=" * 70)


if __name__ == "__main__":
    main()

