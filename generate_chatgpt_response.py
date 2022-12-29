import os, re
import openai
from dotenv import load_dotenv

load_dotenv()

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

def generate_gpt_response(prompt, max_tokens=1500, temperature=1):
  completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=temperature)
    # max_tokens=1500,
    # n=1,
    # stop=None,
    # temperature=1)
  response = completion.choices[0].text
  return response

def get_filename_safe_text(text, num_words=5):
  # Split the text into words
  words = text.split()

  # Get the first `num_words` words
  filename_safe_text = ' '.join(words[:num_words])

  # Replace any non-alphanumeric characters with an underscore
  filename_safe_text = re.sub(r'[^\w]', '_', filename_safe_text)

  return filename_safe_text

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
  filename =  get_filename_safe_text(prompt)
  now = datetime.datetime.now()
  date_time_str = now.strftime("%Y-%m-%d")
  with open(f"gpt-text/{date_time_str}-{filename}.txt", "w") as file:
    file.write("text")
  print(response)