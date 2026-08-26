import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

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
args = parser.parse_args()
# Now we can access `args.user_prompt`

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ],
)

if response.usage == None:
     raise RuntimeError("failed API request")

print(f"Prompt tokens: {response.usage.prompt_tokens} \n" 
      f"Response tokens: {response.usage.completion_tokens} \n"
      f"Response: \n{response.choices[0].message.content}")

#print(response.choices[0].message.content)
    

#if __name__ == "__main__":
    #main()
