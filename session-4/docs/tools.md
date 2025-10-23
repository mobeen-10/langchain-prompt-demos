# Understanding LangChain Tools

## What are LangChain Tools?

A Tool in LangChain is an interface that allows an LLM to interact with external systems or perform specific actions. Think of tools as "capabilities" you give to your agent.

## Key Components of a Tool

1. **Name**: Unique identifier for the tool
2. **Description**: Tells the LLM what the tool does and when to use it
3. **Args Schema**: Defines the input parameters (using Pydantic)
4. **_run method**: The actual implementation/action the tool performs

## Why Tool Descriptions Matter

The description field is **CRITICAL** because:

1. The agent reads ALL tool descriptions to understand what's available
2. Based on the description, the agent decides which tool to use
3. A good description should:
   - Clearly state what the tool does
   - Explain when to use it
   - Mention any important constraints or requirements

### Example of a BAD description:
```
"Calculator tool"  # Too vague - doesn't explain what it does
```

### Example of a GOOD description:
```
"Performs basic arithmetic operations (add, subtract, multiply, divide) 
on two numbers. Use this when you need to do math calculations."
```

## How Agents Use Tools

When you give tools to an agent, here's what happens:

1. The agent receives a user query
2. The agent reads ALL tool descriptions
3. The agent decides which tool to use based on:
   - The query
   - The tool descriptions
   - The current context
4. The agent calls the tool with appropriate parameters
5. The agent receives the tool's output
6. The agent uses that output to continue reasoning

### Example Flow:
```
User: "What's 15 times 8?"

Agent thinks:
- I need to do a calculation
- I have a calculator tool
- I'll use it with a=15, b=8, operation=multiply

Agent calls: calculator.run({"a": 15, "b": 8, "operation": "multiply"})

Tool returns: "15 multiply 8 = 120"

Agent responds: "15 times 8 equals 120"
```

## Best Practices

1. **Always use Field descriptions** - The agent reads these to understand parameters
2. **Use appropriate types** - str, int, float, bool, list, dict
3. **Add validation when needed** - Use Field constraints (ge, le, gt, lt)
4. **Keep models simple** - Don't nest too deeply
5. **Provide defaults when appropriate** - Makes tools easier to use
