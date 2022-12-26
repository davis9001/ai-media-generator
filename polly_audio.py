import requests
import os
from dotenv import load_dotenv
import boto3
import datetime
import re

load_dotenv()

now = datetime.datetime.now()

# Amazon Polly API key
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Function to convert a text script to audio using Amazon Polly
def generate_audio(text, filename, format, voice='Matthew'):
  polly_client = boto3.Session(
                  aws_access_key_id=AWS_ACCESS_KEY_ID,                     
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='us-west-2').client('polly')

  response = polly_client.synthesize_speech(VoiceId=voice,
                OutputFormat=format, 
                Text = text,
                Engine = 'neural')

  file = open(filename, 'wb')
  file.write(response['AudioStream'].read())
  file.close()
  return file

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
  parser.add_argument("text", nargs='?', default=None, help="Input Text")
  args = parser.parse_args()

  if args.text is None:
    # Prompt the user for input if the input argument is not provided
    args.text = input("Enter the script text: ")
  input_text = args.text
  date_time_str = now.strftime("%Y-%m-%d")
  firstwords = get_filename_safe_text(input_text, 5)
  filename = f"polly-audio/{date_time_str}-{firstwords}.mp3"
  generate_audio(input_text, filename, 'mp3')
  print(f"Audio file saved as {filename}.")