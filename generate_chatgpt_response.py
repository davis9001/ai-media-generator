import os
import openai
from dotenv import load_dotenv

load_dotenv()

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

def generate_gpt_response(prompt):
  completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1500,
    temperature=1)
    # max_tokens=1500,
    # n=1,
    # stop=None,
    # temperature=1)
  response = completion.choices[0].text
  return response


if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("prompt", nargs='?', default=None, help="Prompt")
  args = parser.parse_args()

  if args.prompt is None:
    args.prompt = input("Enter the ChatGPT prompt: ")
  prompt = args.prompt
  response = generate_gpt_response(prompt)
  print(response)