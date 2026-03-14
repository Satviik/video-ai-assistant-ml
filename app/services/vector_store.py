import faiss
import numpy as np
import pickle


def store_embeddings(video_id, chunks, embeddings):

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, f"data/vector_db/{video_id}.index")

    with open(f"data/vector_db/{video_id}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)