import anthropic
import os
from dotenv import load_dotenv
from weather import get_weather
from currency import convert_currency, get_dollar_rate
from gold import get_gold_rate
from news import get_latest_news

load_dotenv()

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=" * 50)
print("   Claude Chatbot — Real Time Data")
print("=" * 50)
print("I can help you with real time data!")
print("  🌤️  Weather  → What is the weather in Chennai?")
print("  💱  Currency → What is the dollar rate today?")
print("  💱  Convert  → Convert 1000 USD to INR")
print("  🥇  Gold     → What is today's gold rate?")
print("  📰  News     → Latest news about technology")
print("Type 'quit' to exit\n")

# Define ALL tools
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for any city in the world. Use when user asks about weather, temperature, rain, or climate in a specific location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city. Example: Chennai, London, Tokyo"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_dollar_rate",
        "description": "Get the current live dollar rate against INR and other currencies. Use when user asks about dollar rate, USD rate, or exchange rates.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another using live exchange rates. Use when user asks to convert money between currencies.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount to convert. Example: 1000"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Currency to convert from. Example: USD, INR, EUR, GBP"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Currency to convert to. Example: INR, USD, EUR, GBP"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    },
    {
        "name": "get_gold_rate",
        "description": "Get current live gold rates in both USD and INR for 22 and 24 carat gold. Use when user asks about gold rate, gold price, or gold today.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_latest_news",
        "description": "Get latest news headlines for any topic. Use when user asks about news, headlines, or current events.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "News topic to search for. Example: technology, sports, business, science, general"
                }
            },
            "required": ["topic"]
        }
    }
]

# Conversation history
history = []

def handle_tool_call(tool_name, tool_input):
    """Call the right function based on what Claude requests"""
    if tool_name == "get_weather":
        return get_weather(tool_input["city"])
    elif tool_name == "get_dollar_rate":
        return get_dollar_rate()
    elif tool_name == "convert_currency":
        return convert_currency(
            tool_input["amount"],
            tool_input["from_currency"],
            tool_input["to_currency"]
        )
    elif tool_name == "get_gold_rate":
        return get_gold_rate()
    elif tool_name == "get_latest_news":
        return get_latest_news(tool_input.get("topic", "general"))
    return "Function not found"

# Main chat loop
while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    history.append({
        "role": "user",
        "content": user_input
    })

    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="You are a helpful assistant with access to real time data. You can get weather, currency rates, gold prices, and latest news. Always use the available tools to get accurate live information.",
        tools=tools,
        messages=history
    )

    # Handle tool calls
    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content
                       if block.type == "tool_use")

        tool_name = tool_use.name
        tool_input = tool_use.input

        print(f"\nClaude is calling: {tool_name}({tool_input})")

        result = handle_tool_call(tool_name, tool_input)
        print(f"Data received!")

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
                    "content": result
                }
            ]
        })

        response = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system="You are a helpful assistant with access to real time data. You can get weather, currency rates, gold prices, and latest news. Always use the available tools to get accurate live information.",
            tools=tools,
            messages=history
        )

    reply = response.content[0].text
    history.append({
        "role": "assistant",
        "content": reply
    })

    print(f"\nClaude: {reply}")
    print("-" * 50)