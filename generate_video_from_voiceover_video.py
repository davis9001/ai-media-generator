import whisper
import whisper.utils as wutils
from moviepy.editor import *
from yt_dlp import YoutubeDL
import generate_chatgpt_response as gcr
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json

load_dotenv()
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

def generate_text_from_audio(audio_file_location, save=True):
  model = whisper.load_model("base")
  options = whisper.DecodingOptions(
    language="en", 
    without_timestamps=False)
  audio = whisper.load_audio(audio_file_location)
  
  # audio = whisper.pad_or_trim(audio)
  mel = whisper.log_mel_spectrogram(audio).to(model.device)
  # result = model.transcribe(audio_file_location, options)
  result = whisper.decode(model, mel, options)
  result = result.text
  wutils.WriteSRT
  if save:
    filename = os.path.basename(audio_file_location)
    save_text_file(f'generated-transcription-text/{filename}.txt', result)
  return result

# def generate_transcript(audio_file):
#     # Load the audio file
#     sound = AudioSegment.from_file(audio_file)

#     # Convert the audio to a 16-bit WAV file with a sample rate of 16 kHz
#     sound = sound.set_channels(1).set_frame_rate(16000)
#     sound.export("audio.wav", format="wav")

#     # Generate a transcript using Whisper
#     with open("audio.wav", "rb") as f:
#         response = whisper.speech_to_text(f.read(), lang="en-US", model="whisper")
#     transcript = response["transcription"]
#     return transcript

# def generate_srt_file(transcript, output_file):
#     lines = transcript.split(".")
#     with open(output_file, "w") as f:
#         for i in range(len(lines)):
#             line = lines[i].strip()
#             if line != "":
#                 start_time = time.strftime("%H:%M:%S", time.gmtime(i))
#                 end_time = time.strftime("%H:%M:%S", time.gmtime(i + 1))
#                 f.write(f"{i + 1}\n{start_time},000 --> {end_time},000\n{line}\n\n")

def save_text_file(output_file_location, text):
  with open(output_file_location, "w") as file:
    file.write(text)

def convert_video_to_audio(videofile_path, audiofile_path):
  video = VideoFileClip(videofile_path)
  audio = video.audio
  audio.write_audiofile(audiofile_path)
  return audiofile_path

def download_youtube_videos(main_subject, search_terms = []):
  downloaded_videos = []
  for search_term in search_terms:
    full_search_phrase = f'{main_subject} {search_term}'
    downloaded_video_path = download_youtube_video(full_search_phrase)
    downloaded_videos.append(downloaded_video_path)

def combine_videos_with_audio(video_sources, audio_file_path):
  audio_clip = moviepy.VideoFileClip(audio_file_path)
  audio_clip_length = audio_clip.duration
  video_sources_count = video_sources_paths.length
  needed_video_clip_length = audio_clip_length / video_sources_count
  # [Audio Clip 60s]
  # [V1][V2][V3][V4]
  for video in video_sources_paths:
    video = moviepy.VideoFileClip(video)
    # video.

def download_youtube_video(search_term):
    # Use the YouTube Data API to search for videos with the given movie name
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=f"'{search_term}'",
        part='snippet',
        type='video',
        videoDefinition='high',
        maxResults=9,
        fields='items(id(videoId))'
    ).execute()

    # Get the video ID of the first search result
    video_id = search_response['items'][0]['id']['videoId']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    URLS = ['https://www.youtube.com/watch?v=' + video_id]
    ydl_opts = {'outtmpl': f"downloaded-videos/{search_term}"}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    
    print(f'Successfully downloaded video for "{search_term}"')

def get_main_subject_matter(text):
  prompt = f'In one phrase (Noun) what is this script talking about? {text}'
  response = gcr.generate_gpt_response(prompt, max_tokens=600)
  print(f'Main Subject Matter: {response}')
  return response

def get_subject_matters(text):
  format = " [{'subject': 'timestamp'}, ... ]"
  prompt = f'From the following script identify the parts of the script that mention a particular subject matter and list out these subject matters including the timestamp of where the mention starts. Return the list as JSON in the format {format}: {text}'
  response = gcr.generate_gpt_response(prompt, max_tokens=1000)
  print(f'Subject Matters: {response}')
  return response

def parse_subject_matters(response):
  subject_json = json.loads(response)
  return subject_json



if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("video", nargs='?', default=None, help="Input Video")
    args = parser.parse_args()

    if args.video is None:
        args.video = input("Enter the path to the video file: ")
    
    video_filename = os.path.basename(args.video)
    audio_file_path = f'audio-separated/{video_filename}.wav'
    audio_file = convert_video_to_audio(args.video, audio_file_path)
    text_file = generate_text_from_audio(audio_file)
    main_subject = get_main_subject_matter(text_file)
    subject_matters = get_subject_matters(text_file)
    video_sources = download_youtube_videos(main_subject, subject_matters)
    # final_video = combine_videos_with_audio(video_sources, audio_file)

# input video file
# convert to audio
# convert audio to text with whisper
# get subjects from text using ChatGPT (see ref1)
# download youtube videos of subjects
# combine clips of youtube videos with audio

# ref1: f'From the following script identify the parts of the script that mention a particular subject matter and list out these subject matters including the timestamp of where the mention starts: {script}'
# ref2: f'In one phrase (Noun) what is this script talking about? {script}'