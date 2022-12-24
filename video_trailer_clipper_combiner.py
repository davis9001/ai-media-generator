import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
import mutagen
from moviepy.audio.io.AudioFileClip import AudioFileClip

def main(movie_name):
    # Set the input and output file paths
    input_audio_file = f"movie-description-audio/{movie_name}.mp3"
    input_video_file = f"movie-trailers/{movie_name}.webm"
    output_file = f"movie-description-videos/{movie_name}.mp4"

    audio_file = AudioFileClip(input_audio_file)

    audio_file_length = audio_file.duration

    # Set the number of clips to grab
    num_clips = 5

    # Set the duration of each clip in seconds
    clip_duration = audio_file_length / num_clips

    # Open the input video using VideoFileClip
    video = VideoFileClip(input_video_file)
    video = video.without_audio()

    # Generate the start times for the clips
    start_times = []
    for i in range(num_clips):
        start_times.append(random.randint(0, int(video.duration) - int(clip_duration)))

    # Extract the clips using VideoFileClip.subclip
    clips = []
    for start_time in start_times:
        clips.append(video.subclip(start_time, start_time + clip_duration))

    # Concatenate the clips into a single video using concatenate_videoclips
    final_clip = concatenate_videoclips(clips)
    final_clip.audio = audio_file

    # Save the final clip to the output file
    final_clip.write_videofile(output_file, codec='libx264')


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
    main(movie_name)
