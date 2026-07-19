import json

from app.vector_store import create_vector_store


TASKS_FILE = "data/tasks.json"


def load_tasks():
    """
    Load tasks from the JSON file.
    """
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    return tasks


def ingest():
    """
    Read tasks and create the FAISS vector store.
    """
    tasks = load_tasks()

    create_vector_store(tasks)

    print(f"Successfully ingested {len(tasks)} task(s).")


if __name__ == "__main__":
    ingest()