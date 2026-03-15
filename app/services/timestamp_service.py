import ollama
import re


def extract_timestamp(question, context, answer):

    prompt = f"""
You are helping extract a timestamp from a video transcript.

Question:
{question}

Answer:
{answer}

Transcript context:
{context}

If the answer refers to a moment in the video, return ONLY the timestamp in seconds.

Example output:
23

If no timestamp is relevant return:
None
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"].strip()

    # extract number if present
    match = re.search(r"\d+", content)

    if match:
        return int(match.group())

    return None