import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(video_id, question, top_k=3):

    index = faiss.read_index(f"data/vector_db/{video_id}.index")

    with open(f"data/vector_db/{video_id}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    question_embedding = model.encode([question])

    distances, indices = index.search(question_embedding, top_k)

    retrieved = [chunks[i] for i in indices[0]]

    return retrieved