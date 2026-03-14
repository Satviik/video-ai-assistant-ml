import whisper


model = whisper.load_model("base")


def transcribe_audio(audio_path):

    result = model.transcribe(audio_path)

    transcript = result["text"]

    segments = result["segments"]

    return transcript, segments