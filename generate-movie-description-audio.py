import requests
import os
import openai
from dotenv import load_dotenv
import boto3

load_dotenv()

# ChatGPT API endpoint
CHATGPT_URL = "https://api.openai.com/v1/chatgpt/generate"

# Amazon Polly API endpoint
POLLY_URL = "https://polly.us-east-1.amazonaws.com/v1/speech"

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

# Amazon Polly API key
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

polly_client = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,                     
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name='us-west-2').client('polly')

# Function to generate a 90-second video script for a movie using ChatGPT
def generate_video_script(movie_name):
  movie_script_prompt = f"Write 4 paragraphs describing the plot inside the movie {movie_name} with no formatting."
  completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt=movie_script_prompt,
    max_tokens=1500,
    temperature=1)
    # max_tokens=1500,
    # n=1,
    # stop=None,
    # temperature=1)
  script = completion.choices[0].text
  print(f"Script: {script}")
  return script

# Function to convert a text script to audio using Amazon Polly
def generate_audio(text, filename, format):
  response = polly_client.synthesize_speech(VoiceId='Matthew',
                OutputFormat=format, 
                Text = text,
                Engine = 'neural')

  file = open(filename, 'wb')
  file.write(response['AudioStream'].read())
  file.close()


# Get the name of the movie from the user
movie_name = input("Enter the name of a movie: ")

# Generate the video script for the movie using ChatGPT
script = generate_video_script(movie_name)

# Convert the script to audio file
generate_audio(script, f"movie-description-audio/{movie_name}.mp3", 'mp3')

print(f"Audio file saved as '{movie_name}.mp3'.")