import json
from pathlib import Path


DATA_FILE = Path("data/projects.json")


def load_projects():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_projects(level, category):
    projects = load_projects()

    results = []

    for project in projects:
        level_match = (
            level == "All"
            or project["level"].lower() == level.lower()
        )

        category_match = (
            category == "All"
            or project["category"].lower() == category.lower()
        )

        if level_match and category_match:
            results.append(project)

    return results