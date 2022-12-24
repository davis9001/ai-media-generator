from yt_dlp import YoutubeDL

from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
load_dotenv()

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

def download_movie_trailer(movie_name):
    # Use the YouTube Data API to search for videos with the given movie name
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=f"{movie_name} official trailer",
        part='snippet',
        type='video',
        videoDefinition='high',
        maxResults=1,
        fields='items(id(videoId))'
    ).execute()

    # Get the video ID of the first search result
    video_id = search_response['items'][0]['id']['videoId']

    # # Use pytube to download the video
    # youtube = pytube.YouTube('https://www.youtube.com/watch?v=' + video_id)
    # video = youtube.streams.first()
    # video.download()
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    URLS = ['https://www.youtube.com/watch?v=' + video_id]
    ydl_opts = {'outtmpl': f"movie-trailers/{movie_name}"}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)

    
    print(f'Successfully downloaded video for "{movie_name}"')


movie_name = input("Input the name of the movie")

download_movie_trailer(movie_name)