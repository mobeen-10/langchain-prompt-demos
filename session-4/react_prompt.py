"""
ReAct Prompt Template

This module contains the standard ReAct prompt template used across all agent examples.
The ReAct pattern requires a specific format for the LLM to follow.
"""

from langchain_core.prompts import PromptTemplate

# Standard ReAct prompt template
REACT_PROMPT = PromptTemplate.from_template("""
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

# Concise ReAct prompt (for simpler examples)
REACT_PROMPT_CONCISE = PromptTemplate.from_template("""
You are a helpful assistant. Use tools only when needed.

Tools:
{tools}

Format:
Question: <user question>
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: {"key": "value"} (valid JSON, no quotes around the whole thing)
Observation: result of the action
... (repeat as needed)
Thought: I now know the final answer
Final Answer: concise final answer

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

def get_react_prompt(concise=False):
    return REACT_PROMPT_CONCISE if concise else REACT_PROMPT
