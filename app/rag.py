from app.vector_store import search_vector_store
from app.prompts import build_prompt


def retrieve(question: str, k: int = 3):
    """
    Retrieve the most relevant tasks from the vector store.
    """
    return search_vector_store(question, k)


def answer_question(question: str):
    """
    Executes the RAG pipeline.

    Currently:
    - Retrieves relevant tasks
    - Builds the LLM prompt

    Later:
    - Sends the prompt to Mistral
    """

    tasks = retrieve(question)

    prompt = build_prompt(
        question=question,
        tasks=tasks
    )

    return {
        "question": question,
        "retrieved_tasks": tasks,
        "prompt": prompt
    }