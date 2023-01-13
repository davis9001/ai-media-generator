import requests
import os
import openai
from dotenv import load_dotenv
import boto3

load_dotenv()


# Amazon Polly API key
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Function to convert a text script to audio using Amazon Polly
def generate_audio(text, filename, format):
  polly_client = boto3.Session(
                  aws_access_key_id=AWS_ACCESS_KEY_ID,                     
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='us-west-2').client('polly')

  response = polly_client.synthesize_speech(VoiceId='Matthew',
                OutputFormat=format, 
                Text = text,
                Engine = 'neural')

  file = open(filename, 'wb')
  file.write(response['AudioStream'].read())
  file.close()
  return file

if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("input", nargs='?', default=None, help="Movie Name (Year)")
  args = parser.parse_args()

  if args.input is None:
    # Prompt the user for input if the input argument is not provided
    args.input = input("Enter the Movie Name (Year): ")
  movie_name = args.input
  with open(f"generated-gpt-text/{movie_name}.txt") as file:
    script = file.read()
  generate_audio(script, f"generated-tts-audio/{movie_name}.mp3", 'mp3')
  print(f"Audio file saved as 'generated-tts-audio/{movie_name}.mp3'.")