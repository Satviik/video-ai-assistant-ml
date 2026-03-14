import ollama


def generate_answer(question, context, history):

    prompt = f"""
You are an AI assistant answering questions about a video.

Use the transcript context to answer the question.

Answer in **1-2 concise sentences**.
Avoid long explanations.

Conversation History:
{history}

Transcript Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]