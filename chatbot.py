import anthropic
import os
import json
from dotenv import load_dotenv
from weather import get_weather

load_dotenv()

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=" * 50)
print("   Claude Chatbot with Function Calling")
print("=" * 50)
print("Ask me anything — including weather questions!")
print("Type 'quit' to exit\n")

# Define the weather function for Claude
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for any city in the world. Use this when the user asks about weather, temperature, or climate in a specific location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for. Example: Chennai, London, New York"
                }
            },
            "required": ["city"]
        }
    }
]

# Conversation history
history = []

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    # Add user message to history
    history.append({
        "role": "user",
        "content": user_input
    })

    # Send to Claude with tools
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="You are a helpful assistant. When users ask about weather, use the get_weather function to get real data.",
        tools=tools,
        messages=history
    )

    # Check if Claude wants to use a function
    if response.stop_reason == "tool_use":
        
        # Get the tool Claude wants to use
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input
        
        print(f"\nClaude is calling: {tool_name}({tool_input})")
        
        # Call our weather function
        if tool_name == "get_weather":
            weather_result = get_weather(tool_input["city"])
            print(f"Weather data received!")
        
        # Add Claude's response and tool result to history
        history.append({
            "role": "assistant",
            "content": response.content
        })
        
        history.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": weather_result
                }
            ]
        })
        
        # Send tool result back to Claude for final answer
        final_response = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system="You are a helpful assistant. When users ask about weather, use the get_weather function to get real data.",
            tools=tools,
            messages=history
        )
        
        reply = final_response.content[0].text
        
        # Save final reply to history
        history.append({
            "role": "assistant",
            "content": reply
        })

    else:
        # Normal response without function calling
        reply = response.content[0].text
        
        history.append({
            "role": "assistant",
            "content": reply
        })

    print(f"\nClaude: {reply}")
    print("-" * 50)