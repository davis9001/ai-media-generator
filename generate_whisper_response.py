import whisper

def generate_text(audio_file_location):
  model = whisper.load_model("base")
  result = model.transcribe(audio_file_location)
  return result["text"]

def save_text_file(output_file_location, text):
  with open(output_file_location, "w") as file:
    file.write(text)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs='?', default=None, help="Input Audio")
    args = parser.parse_args()

    if args.input is None:
        # Prompt the user for input if the input argument is not provided
        args.input = input("Enter the path to the audio file: ")
    
    audio_file_location = args.input
    text = generate_text(audio_file_location)
    filename = os.path.basename(audio_file_location)
    save_text_file(f'generated-whisper-text/{filename}.txt', text)
