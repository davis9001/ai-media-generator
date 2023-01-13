This project uses Python 3.8.

## Environment Installation:
```
$ git clone git@github.com:davis9001/ai-media-generator.git
$ cd ai-media-generator
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

You will need to create a `.env` file which includes the API keys for the needed services.

Copy the `.env.example` file to `.env` and fill in the keys.

## Running:
There are currently four separate python scripts that will do the following:
1) Download the first result for `MOVIE_NAME official trailer 1080p` from YouTube.
2) Generate a description of MOVIE_NAME from OpenAI and save it as a text file.
3) Generate an audio file from the text description using text-to-speech on that from Amazon Polly.
4) Combine the audio track (text-to-speech) with random clips selected from the movie trailer.

Each of these will save the files into four separate folders (and the files are not automatically deleted).
1) `movie-trailers`
2) `generated-gpt-text`
3) `generated-tts-audio`
4) `generated-movie-description-video`

The should be run in the following order (at least the text needs to be generated before the audio, and the audio before the video...)
```
$ python download_movie_trailer.py 'Movie Name (Year)'
$ python generate_movie_description_text.py 'Movie Name (Year)'
$ python generate_movie_description_audio.py 'Movie Name (Year)'
$ python generate_movie_description_video.py 'Movie Name (Year)'
```

## Miscelaneous

A script for generating arbritary ChatGPT responses has been added as well.
```
$ python generate_chatgpt_response.py 'PROMPT'
```

Each response from `generate_chatgpt_response.py` will be saved as txt files in the `gpt-text` folder with a timestamp and the first few words of the request as the filename.
