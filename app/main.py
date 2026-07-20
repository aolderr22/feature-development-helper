from pathlib import Path

from app.tools import check_task_availability
from app.task_config import get_task


def determine_task(user_input):
    """
    Determines the task_id from the user's request.

    This is a temporary classifier.
    Later this can be replaced with an LLM tool call.
    """

    user_input = user_input.lower()

    tasks = {
        "pdf": "pdf_refactor",
        "hco": "hco_update",
        "hco_id": "hco_update"
    }

    for keyword, task_id in tasks.items():
        if keyword in user_input:
            return task_id

    return None


def load_notes(task_id):
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


def process_request(user_input):
    """
    Main application workflow.
    """

    task_id = determine_task(user_input)

    if task_id is None:
        return (
            "I could not determine the task. "
            "Please specify a software task."
        )


    availability = check_task_availability(task_id)


    if not availability["approved"]:

        return (
            f"Today is {availability['current_date']}. "
            f"{availability['reason']} "
            f"Please choose another task."
        )


    notes = load_notes(task_id)


    return (
        "This task is approved.\n\n"
        "Here are the notes for completing it:\n\n"
        f"{notes}"
    )


if __name__ == "__main__":

    while True:

        user_input = input("\nWhat task do you want to work on?\n> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = process_request(user_input)

        print("\nAI Response:")
        print(response)