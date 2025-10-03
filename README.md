# Task-CLI: A Simple Command-Line Task Tracker

This is a lightweight, command-line task management tool built with Python. It allows you to easily add, track, and manage your tasks directly from the terminal.

## Features

*   **Add, Update, and Delete Tasks:** Quickly add new tasks, modify existing ones, or remove them when completed.
*   **Track Task Status:** Mark tasks as "todo", "in-progress", or "done" to keep track of your workflow.
*   **List and Filter Tasks:** View all your tasks or filter them by status to see what you need to work on next.
*   **Persistent Storage:** Your tasks are saved in a local SQLite database (`tasks.db`), so you won't lose them.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/task-cli.git
    cd task-cli
    ```

2.  **Recommended: Set up a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies (though this project has no external ones):**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Note: You may need to create a `requirements.txt` file if you add dependencies later.)*

## Usage

The script is executed using `main.py`. Here are the available commands:

*   **Add a new task:**
    ```bash
    python3 main.py add "Your new task description"
    ```

*   **Update a task's description:**
    ```bash
    python3 main.py update <task_id> "The new description"
    ```

*   **Delete a task:**
    ```bash
    python3 main.py delete <task_id>
    ```

*   **Mark a task with a status:**
    ```bash
    python3 main.py mark <task_id> <status>
    ```
    *   `<status>` can be `todo`, `in-progress`, or `done`.

*   **List all tasks:**
    ```bash
    python3 main.py list
    ```

*   **List tasks with a specific status:**
    ```bash
    python3 main.py list <status>
    ```
    *   Example: `python3 main.py list todo`

## Dependencies

*   **Python 3.12+**

This project uses only the standard Python libraries (`sqlite3`, `argparse`, `datetime`), so no external packages are required.
