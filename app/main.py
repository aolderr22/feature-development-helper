from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from app.tools import check_task_availability
from app.task_config import get_task

app = FastAPI(title="Feature Development Helper")

class TaskRequest(BaseModel):
    user_input: str

def determine_task(user_input: str):
    """
    Determines the task_id from the user's request.

    This is a temporary classifier.
    Later this can be replaced with embeddings or an LLM.
    """

    user_input = user_input.lower()

    tasks = {
        "pdf": "pdf_refactor",
        "hco": "hco_update",
        "hco_id": "hco_update",
    }

    for keyword, task_id in tasks.items():
        if keyword in user_input:
            return task_id

    return None


def load_notes(task_id: str):
    """
    Loads task-specific notes from the location
    defined in tasks.json.
    """

    task = get_task(task_id)

    if task is None:
        return "No task configuration found."

    notes_file = Path(task["notes_file"])

    if not notes_file.exists():
        return "No notes file found for this task."

    return notes_file.read_text()


def process_request(user_input: str):
    """
    Main application workflow.
    """

    task_id = determine_task(user_input)

    if task_id is None:
        return {
            "response": (
                "I could not determine the task. "
                "Please specify a software task."
            )
        }

    availability = check_task_availability(task_id)

    task = get_task(task_id)
    prerequisite_note = ""

    if task_id == "pdf_refactor" and task is not None:
        prerequisites = task.get("prerequisites", [])
        if prerequisites:
            prerequisite_note = (
                "Prerequisites: "
                + ", ".join(prerequisites)
                + "."
            )

    if not availability["approved"]:
        return {
            "response": (
                f"Today is {availability['current_date']}. "
                f"{availability['reason']} "
                f"Please choose another task."
                f"\n\n{prerequisite_note}" if prerequisite_note else ""
            )
        }

    notes = load_notes(task_id)

    return {
        "response": (
            "This task is approved.\n\n"
            f"{prerequisite_note}\n\n"
            "Here are the notes for completing it:\n\n"
            f"{notes}"
        )
    }


@app.get("/")
def root():
    return {
        "message": "Feature Development Helper API is running."
    }

@app.post("/task")
def task(request: TaskRequest):
    return process_request(request.user_input)

if __name__ == "__main__":

    while True:

        user_input = input("\nWhat task do you want to work on?\n> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = process_request(user_input)

        print("\nAI Response:")
        print(response["response"])