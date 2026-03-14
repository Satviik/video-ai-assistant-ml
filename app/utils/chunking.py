def chunk_transcript_segments(segments, window_size=4):

    chunks = []

    for i in range(len(segments) - window_size + 1):

        group = segments[i:i + window_size]

        start = int(group[0]["start"])

        text = " ".join(seg["text"].strip() for seg in group)

        if len(text.split()) > 8:
            chunk = f"[{start}s] {text}"
            chunks.append(chunk)

    return chunks