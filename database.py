import sqlite3
import json
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "project_data.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            project_data TEXT NOT NULL,
            progress INTEGER DEFAULT 0,
            completed_tasks TEXT DEFAULT '[]',
            tech_stack TEXT DEFAULT '[]',
            database_tables TEXT DEFAULT '[]',
            project_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# SAVE PROJECT
# ============================================================

def save_project(
    project,
    progress=0,
    completed_tasks=None,
    tech_stack=None,
    database_tables=None,
    project_notes=""
):

    if completed_tasks is None:
        completed_tasks = []

    if tech_stack is None:
        tech_stack = []

    if database_tables is None:
        database_tables = []

    project_name = project.get(
        "name",
        project.get(
            "title",
            "Untitled Project"
        )
    )

    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects (
            project_name,
            project_data,
            progress,
            completed_tasks,
            tech_stack,
            database_tables,
            project_notes,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(project_name)
        DO UPDATE SET
            project_data = excluded.project_data,
            progress = excluded.progress,
            completed_tasks = excluded.completed_tasks,
            tech_stack = excluded.tech_stack,
            database_tables = excluded.database_tables,
            project_notes = excluded.project_notes,
            updated_at = excluded.updated_at
        """,
        (
            project_name,
            json.dumps(project),
            progress,
            json.dumps(completed_tasks),
            json.dumps(tech_stack),
            json.dumps(database_tables),
            project_notes,
            now,
            now,
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# LOAD ALL SAVED PROJECTS
# ============================================================

def load_saved_projects():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM projects
        ORDER BY updated_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    projects = []

    for row in rows:

        project = json.loads(
            row["project_data"]
        )

        projects.append(
            {
                "project": project,

                "progress": row["progress"],

                "completed_tasks": json.loads(
                    row["completed_tasks"] or "[]"
                ),

                "tech_stack": json.loads(
                    row["tech_stack"] or "[]"
                ),

                "database_tables": json.loads(
                    row["database_tables"] or "[]"
                ),

                "project_notes": (
                    row["project_notes"] or ""
                ),

                "created_at": row["created_at"],

                "updated_at": row["updated_at"],
            }
        )

    return projects


# ============================================================
# LOAD ONE PROJECT
# ============================================================

def load_project(project_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM projects
        WHERE project_name = ?
        """,
        (project_name,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "project": json.loads(
            row["project_data"]
        ),

        "progress": row["progress"],

        "completed_tasks": json.loads(
            row["completed_tasks"] or "[]"
        ),

        "tech_stack": json.loads(
            row["tech_stack"] or "[]"
        ),

        "database_tables": json.loads(
            row["database_tables"] or "[]"
        ),

        "project_notes": (
            row["project_notes"] or ""
        ),

        "created_at": row["created_at"],

        "updated_at": row["updated_at"],
    }


# ============================================================
# DELETE PROJECT
# ============================================================

def delete_project(project_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM projects
        WHERE project_name = ?
        """,
        (project_name,)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# ============================================================
# COUNT PROJECTS
# ============================================================

def get_project_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM projects"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ============================================================
# INITIALIZE DATABASE WHEN MODULE LOADS
# ============================================================

init_database()