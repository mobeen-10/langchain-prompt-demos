# Understanding Agent Scratchpad

## What is the Agent Scratchpad?

The agent scratchpad is the agent's "working memory" - it contains the complete reasoning history of what the agent has thought, what actions it has taken, and what observations it has received.

## The ReAct Format

The scratchpad follows the ReAct (Reasoning + Acting) format:

```
Thought: I need to calculate 10 + 5
Action: calculator
Action Input: 10 + 5
Observation: 15

Thought: I now know the final answer
Final Answer: 15
```

## Key Components

1. **Thought**: The agent's reasoning about what to do next
2. **Action**: The tool the agent decides to use
3. **Action Input**: The parameters for the tool
4. **Observation**: The result from the tool
5. **Final Answer**: The agent's final response to the user

## Why the Scratchpad Matters

The scratchpad is crucial because:

1. **Context Preservation**: Each thought builds on previous observations
2. **Debugging**: You can see exactly how the agent reasoned
3. **Learning**: The agent can reference its own previous steps
4. **Consistency**: Ensures the agent follows a structured reasoning process

## Example: Multi-Step Reasoning

```
Question: What is 20 + 10, then subtract 5, then multiply by 2?

Thought: I need to calculate 20 + 10 first
Action: calculator
Action Input: 20 + 10
Observation: 30

Thought: Now I need to subtract 5 from 30
Action: calculator
Action Input: 30 - 5
Observation: 25

Thought: Finally, I need to multiply 25 by 2
Action: calculator
Action Input: 25 * 2
Observation: 50

Thought: I now know the final answer
Final Answer: 50
```

## How the Agent Uses the Scratchpad

1. **Reads previous steps** to understand what it has already done
2. **Builds on observations** to make the next decision
3. **Avoids repeating actions** by checking its history
4. **Maintains context** throughout the entire conversation

## Key Takeaways

- The scratchpad is the agent's working memory
- It follows the Thought → Action → Observation pattern
- Each step builds on previous observations
- It enables complex multi-step reasoning
- It's essential for debugging and understanding agent behavior
