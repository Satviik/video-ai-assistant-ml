import json


def save_transcript(video_id, segments):

    path = f"data/transcripts/{video_id}.json"

    with open(path, "w") as f:
        json.dump(segments, f, indent=2)

    return path