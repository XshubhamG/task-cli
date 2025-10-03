#!/usr/bin/env python3

import sqlite3
import argparse
import datetime

DB_FILE = "tasks.db"


# Initialize the database and create the tasks table
def init_db():
    """Initializes the database and creates the tasks table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Use IF NOT EXISTS to prevent errors on subsequent runs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('todo', 'in-progress', 'done')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # A trigger to automatically update the updated_at timestamp
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_task_updated_at
            AFTER UPDATE ON tasks
            FOR EACH ROW
            BEGIN
                UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)
        conn.commit()


# Add a sample function to add a task
def add_task(description):
    """Adds a new task to the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (description, status) VALUES (?, ?)",
            (description, "todo"),
        )
        conn.commit()
        print(f"Task added successfully (ID: {cursor.lastrowid})")


# Function to update a task's description
def update_task(task_id, new_description):
    """Updates the description of an existing task."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Task {task_id} updated successfully.")


# Function to delete a task
def delete_task(task_id):
    """Deletes a task from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Task {task_id} deleted successfully.")


# Function to update a task's status
def update_task_status(task_id, status):
    """Updates the status of a task."""
    if status not in ["todo", "in-progress", "done"]:
        print("Error: Invalid status. Choose from 'todo', 'in-progress', or 'done'.")
        return

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Task {task_id} marked as '{status}'.")


# Function to list all tasks
def list_tasks(status_filter=None):
    """Lists tasks, optionally filtering by status."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        query = "SELECT id, description, status, created_at FROM tasks"
        params = []
        if status_filter:
            query += " WHERE status = ?"
            params.append(status_filter)

        cursor.execute(query, params)
        tasks = cursor.fetchall()

        if not tasks:
            if status_filter:
                print(f"No tasks with status '{status_filter}'.")
            else:
                print("No tasks found.")
            return

        print(f"{'ID':<4} | {'Status':<12} | {'Description'}")
        print("-" * 50)
        for task in tasks:
            print(f"{task[0]:<4} | {task[2]:<12} | {task[1]}")


def main():
    # Always make sure the DB is ready
    init_db()

    parser = argparse.ArgumentParser(description="A simple command-line task tracker.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Command: add
    parser_add = subparsers.add_parser("add", help="Add a new task.")
    parser_add.add_argument(
        "description", type=str, help="The description of the task."
    )

    # Command: update
    parser_update = subparsers.add_parser(
        "update", help="Update an existing task's description."
    )
    parser_update.add_argument("id", type=int, help="The ID of the task to update.")
    parser_update.add_argument(
        "description", type=str, help="The new description for the task."
    )

    # Command: delete
    parser_delete = subparsers.add_parser("delete", help="Delete a task.")
    parser_delete.add_argument("id", type=int, help="The ID of the task to delete.")

    # Command: mark (as todo, in-progress, or done)
    parser_mark = subparsers.add_parser("mark", help="Mark a task with a status.")
    parser_mark.add_argument("id", type=int, help="The ID of the task to mark.")
    parser_mark.add_argument(
        "status",
        type=str,
        choices=["todo", "in-progress", "done"],
        help="The new status.",
    )

    # Command: list
    parser_list = subparsers.add_parser("list", help="List tasks.")
    parser_list.add_argument(
        "status",
        type=str,
        nargs="?",
        default=None,
        choices=["todo", "in-progress", "done"],
        help="Filter tasks by status.",
    )

    args = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark":
        update_task_status(args.id, args.status)
    elif args.command == "list":
        list_tasks(args.status)


if __name__ == "__main__":
    main()
