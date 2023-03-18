import random
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.config import change_settings
# change_settings({"IMAGEMAGICK_BINARY": r"/usr/local/bin/convert"})
from skimage.filters import gaussian


def make_landscape_video(movie_name):
    # Set the input file paths
    input_audio_file = f"generated-tts-audio/{movie_name}.mp3"
    input_video_file = f"movie-trailers/{movie_name}.webm"

    # Open the input video (trailer)
    video_file = VideoFileClip(input_video_file)
    video_file = video_file.without_audio()

    video_length = video_file.duration

    # Open the input audio (voiceover)
    audio_file = AudioFileClip(input_audio_file)

    audio_file_length = audio_file.duration

    # Set the number of clips to grab
    num_clips = 4

    # Create start times as equally spaced num_clips into audio_file_length
    # e.g. [0, 9, 19, 28, 38]
    start_times = create_start_times(num_clips, video_length)

    # Set the duration of each clip in seconds
    clip_duration = audio_length / num_clips


    # Extract the clips using VideoFileClip.subclip
    clips = []

    # Offset the start of each clip by:
    clip_offset = 2
    for start_time in start_times:
        start_time = start_time + clip_offset
        clips.append(video_file.subclip(start_time, start_time + clip_duration))

    # Concatenate the clips into a single video using concatenate_videoclips
    final_clip = concatenate_videoclips(clips)
    final_clip.audio = audio_file
    final_clip = final_clip.resize(width=1920)

    return final_clip

def write_landscape_video(video_clip, movie_name):
    # Set output file path
    output_file = f"generated-movie-description-videos/{movie_name}.mp4"

    # Save the final clip to the output file
    video_clip.write_videofile(output_file, codec='libx264')

def make_portrait_video(landscape_clip, movie_name):
    landscape_duration = landscape_clip.duration

    if landscape_duration > 59:
        print('Duration over 59 seconds, speeding up...')
        landscape_clip = landscape_clip.fx( vfx.speedx, landscape_duration/59)
    
    blank_portrait_clip = ColorClip(
        (1080, 1920),
        color=(0,0,0),
        duration=landscape_clip.duration)

    # movie_title_text = TextClip(movie_name, fontsize=24, color='white', font='Dosis')
    # movie_title_text.set_duration(landscape_clip.duration)
    landscape_clip_blurred = landscape_clip.fl_image( blur )
    final_clip = CompositeVideoClip(
        [
            blank_portrait_clip,
            landscape_clip_blurred.set_position("center").resize(2.3),
            landscape_clip.set_position("center").resize(0.5625),
            # movie_title_text
            ], size=[1080,1920], use_bgclip=True)

    return final_clip


def write_portrait_video(portrait_clip, movie_name):
    output_file = f"generated-movie-description-videos/{movie_name} - PORTRAIT.mp4"
    
    portrait_clip.write_videofile(output_file, codec='libx264')

def blur(image):
    return gaussian(image.astype(float), sigma=9)

def create_start_times(n, x):
    # Create start times as equally spaced num_clips (n) into movie_trailer_length (x)
    # for n=5 and x=60
    # return [0, 9, 19, 28, 38]
    step = x/n
    return [int(i*step) for i in range(n)]

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
    landscape_clip = make_landscape_video(movie_name)
    portrait_clip = make_portrait_video(landscape_clip, movie_name)
    write_landscape_video(landscape_clip, movie_name)
    write_portrait_video(portrait_clip, movie_name)
