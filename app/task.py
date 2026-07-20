class Task:
    def __init__(self, name, available_after, prerequisites, notes_file, story_url):
        self.name = name
        self.available_after = available_after
        self.prerequisites = prerequisites
        self.notes_file = notes_file
        self.story_url = story_url