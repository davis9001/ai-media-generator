from dotenv import load_dotenv
import openai
import os
from generate_chatgpt_response import *

load_dotenv()

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

# Function to generate a 90-second video script for a movie using ChatGPT
def generate_video_script(movie_name, filename):
  movie_script_prompt = f"""Please Write a script for a youtube short describing the movie {movie_name} from the perspective of inside the movie (don't mention any actors or the production). Make the script take 55 seconds or less for Amazon Polly to read and be accurate about the actual plot of the movie. Only include the narration script without any screen direction or the name of the narrator. Don't ask questions about the plot just describe and spoil it outright. Don't ask the viewer to like or subscribe or anything like that just stick to the movie plot and be brief about it.
"""
  
  script = generate_gpt_response(movie_script_prompt, temperature=1)
  
  print(f"Script: {script}")
  
  with open(filename, "w") as file:
    file.write(script)

  return script


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
  script = generate_video_script(movie_name, f"generated-gpt-text/{movie_name}.txt")
