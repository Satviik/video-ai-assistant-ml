import ollama


def rewrite_query(question):

    prompt = f"""
Rewrite the user's question to improve semantic search in a video transcript.

Rules:
- Keep the same meaning
- Make it clear and descriptive
- Do not answer the question
- Only return the rewritten question

User question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    rewritten = response["message"]["content"].strip()

    return rewritten