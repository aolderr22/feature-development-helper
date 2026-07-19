import os
import pickle
import faiss
import numpy as np

from app.embeddings import create_embedding

VECTOR_STORE_PATH = "vector_store/tasks.index"
METADATA_PATH = "vector_store/tasks_metadata.pkl"

def create_vector_store(tasks):
    """
    Creates a FAISS vector store from task data.

    Args:
        tasks: List of task dictionaries

    Returns:
        FAISS index
    """

    embeddings = []
    metadata = []

    for task in tasks:
        text = (
            f"{task['task']} "
            f"{task['description']} "
            f"{task['availabilityPrerequisite']}"
        )

        embedding = create_embedding(text)

        embeddings.append(embedding)
        metadata.append(task)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    os.makedirs("vector_store", exist_ok=True)

    faiss.write_index(
        index,
        VECTOR_STORE_PATH
    )

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    return index


def load_vector_store():
    """
    Loads an existing FAISS vector store.
    """

    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(
            "Vector store does not exist. Run ingestion first."
        )

    index = faiss.read_index(
        VECTOR_STORE_PATH
    )

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search_vector_store(query, k=3):
    """
    Searches the FAISS vector store.

    Args:
        query: User question
        k: Number of results

    Returns:
        Matching tasks
    """

    index, metadata = load_vector_store()

    query_embedding = create_embedding(query)

    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")


    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx in indices[0]:

        if idx < len(metadata):
            results.append(
                metadata[idx]
            )

    return results