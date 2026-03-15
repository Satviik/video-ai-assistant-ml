def chunk_transcript_segments(segments, window_size=6):

    chunks = []

    for i in range(len(segments) - window_size + 1):

        group = segments[i:i + window_size]

        start_time = int(group[0]["start"])

        text = " ".join(seg["text"].strip() for seg in group)

        chunk = f"[{start_time}s] {text}"

        chunks.append(chunk)

    return chunks