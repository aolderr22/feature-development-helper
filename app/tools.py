from datetime import datetime
from app.task_config import get_task

def get_current_date():

    return datetime.now().strftime("%m/%d/%Y")


def check_task_availability(task_id):

    task = get_task(task_id)

    if task is None:
        return {
            "approved": False,
            "reason": "Unknown task."
        }

    current_date = datetime.now().date()


    available_after = datetime.strptime(
        task["available_after"],
        "%Y-%m-%d"
    ).date()

    if current_date < available_after:

        return {
            "approved": False,
            "current_date": current_date.strftime("%m/%d/%Y"),
            "available_after": available_after.strftime("%m/%d/%Y"),
            "reason": (
                f"{task['name']} is not available yet."
            )
        }


    return {
        "approved": True,
        "current_date": current_date.strftime("%m/%d/%Y"),
        "reason": "Task is available."
    }