SYSTEM_PROMPT = """
You are Feature Development Helper.

You answer questions for software engineers using ONLY the retrieved task information.

If the retrieved information does not answer the user's question, say that you do not have enough information.

Be concise and accurate.
""".strip()


def build_prompt(question: str, tasks: list) -> str:
    """
    Builds a prompt for the language model.
    """

    context = ""

    for task in tasks:
        context += (
            f"Task: {task['task']}\n"
            f"Description: {task['description']}\n"
            f"Date Available: {task['dateAvailable']}\n"
            f"Prerequisite: {task['availabilityPrerequisite']}\n\n"
        )

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved Tasks
----------------
{context}

User Question
-------------
{question}

Answer:
"""

    return prompt.strip()