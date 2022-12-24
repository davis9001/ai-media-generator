This project uses Python 3.8.

## Environment Installation:
```
$ git clone git@github.com:davis9001/ai-media-generator.git
$ cd ai-media-generator
$ python -m env env
$ source env/bin/activate
$ pip install -r requirements.txt
```

There are currently three separate python scripts that will do the following:
1) Download the first result for MOVIE_NAME from YouTube
2) Generate a description of MOVIE_NAME from OpenAI then run text-to-speech on that from Amazon Polly
3) Combine the audio track (text-to-speech) with random clips selected from the movie trailer

Each of these will save the files into three separate folders (and the files are not automatically deleted).
1) movie-trailers
2) movie-description-audio
3) movie-description-video

## Running:
```
$ python download-movie-trailer.py
$ python generate-movie-description-audio.py
$ python video-trailer-clipper-combiner.py
```

