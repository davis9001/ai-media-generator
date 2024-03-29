import os, re
import openai
from dotenv import load_dotenv
import datetime

load_dotenv()

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

def generate_gpt_response(prompt, max_tokens=3999, temperature=0.9):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
      "role": "user",
      "content": prompt
    }]
  )
  response = completion.choices[0].message.content
  return response

def get_filename_safe_text(text, num_words=5):
  # Split the text into words
  words = text.split()

  # Get the first `num_words` words
  filename_safe_text = ' '.join(words[:num_words])

  # Replace any non-alphanumeric characters with an underscore
  filename_safe_text = re.sub(r'[^\w]', '_', filename_safe_text)

  now = datetime.datetime.now()
  date_time_str = now.strftime("%Y-%m-%d")

  return f"{date_time_str}-{filename_safe_text}"

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

  # Write the response to file
  filename =  get_filename_safe_text(prompt)
  with open(f"generated-gpt-text/{filename}.txt", "w") as file:
    file.write(response)
  
  print(response)