This project uses Python 3.8.

## Environment Installation:
```
$ git clone git@github.com:davis9001/ai-media-generator.git
$ cd ai-media-generator
$ python -m env env
$ source env/bin/activate
$ pip install -r requirements.txt
```

You will need to create a `.env` file which includes the API keys for the needed services.

Rename or copy the `.env.example` file to `.env` and fill in the keys.

## Running:
There are currently three separate python scripts that will do the following:
1) Download the first result for MOVIE_NAME from YouTube
2) Generate a description of MOVIE_NAME from OpenAI then run text-to-speech on that from Amazon Polly
3) Combine the audio track (text-to-speech) with random clips selected from the movie trailer

Each of these will save the files into three separate folders (and the files are not automatically deleted).
1) movie-trailers
2) movie-description-audio
3) movie-description-video

```
$ python download_movie_trailer.py
$ python generate_movie_description_audio.py
$ python video_trailer_clipper_combiner.py
```

