chat_memory = {}


def add_message(video_id, role, message):

    if video_id not in chat_memory:
        chat_memory[video_id] = []

    chat_memory[video_id].append({
        "role": role,
        "message": message
    })


def format_history(video_id):

    history = chat_memory.get(video_id, [])

    formatted = ""

    for msg in history:
        formatted += f"{msg['role']}: {msg['message']}\n"

    return formatted