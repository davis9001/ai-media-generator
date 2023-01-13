from dotenv import load_dotenv
import openai
import os

load_dotenv()

# ChatGPT API key
openai.organization = os.getenv("CHATGPT_ORG")
openai.api_key = os.getenv("CHATGPT_API_KEY")

# Function to generate a 90-second video script for a movie using ChatGPT
def generate_video_script(movie_name, filename):
  movie_script_prompt = f"Write four long paragraphs of voiceover script accurately describing the plot from the screenplay of the movie {movie_name} without mentioning the actors or the production. Mention at the beginning that this video contains spoilers in just a few words."
  completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt=movie_script_prompt,
    max_tokens=1800,
    temperature=0.96)
    # max_tokens=1500,
    # n=1,
    # stop=None,
    # temperature=1)
  script = completion.choices[0].text
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
  script = generate_video_script(movie_name, f"movie-description-text/{movie_name}.txt")
