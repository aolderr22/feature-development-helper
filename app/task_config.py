import json
from pathlib import Path

TASK_CONFIG_PATH = Path("data/tasks.json")

def load_tasks():
    """
    Loads task definitions from tasks.json.

    Returns:
        dict: Task definitions keyed by task_id
    """

    with open(TASK_CONFIG_PATH, "r") as file:
        data = json.load(file)

    return data["tasks"]


def get_task(task_id):
    """
    Retrieves a single task definition.

    Args:
        task_id (str): The unique task identifier.

    Returns:
        dict | None: Task configuration or None if not found.
    """

    tasks = load_tasks()

    return tasks.get(task_id)