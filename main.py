import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
            raise RuntimeError("API Key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("failed API request")

    message = response.choices[0].message

    if message.tool_calls == None or len(message.tool_calls) == 0:
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt} \n"
                f"Prompt tokens: {response.usage.prompt_tokens} \n" 
            f"Response tokens: {response.usage.completion_tokens} \n"
            f"Response: \n{response.choices[0].message.content}")
        else:
            print(f"Response: \n{response.choices[0].message.content}")

    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")


    

if __name__ == "__main__":
    main()
