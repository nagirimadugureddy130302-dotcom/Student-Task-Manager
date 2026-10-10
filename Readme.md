# StudyTrack — Student Task Manager

A beginner-friendly task manager built with Python, Flask, SQLite, HTML, and CSS.

## Features

- Add, view, edit, and delete tasks
- Mark tasks completed or pending
- Save tasks in a local SQLite database
- Search tasks by title or subject
- Filter by status and priority
- Dashboard statistics and completion progress bar
- Overdue task indicators
- Responsive layout for desktop and mobile
- Form validation and confirmation before deletion

## Requirements

- Python 3.10 or newer
- pip

## Run on Windows (PowerShell)

1. Open this folder in VS Code.
2. Open the VS Code terminal (`Terminal` → `New Terminal`).
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt in VS Code and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install Flask:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python app.py
   ```

7. Open `http://127.0.0.1:5000/` in your browser.

Keep the terminal running while using the app. Press `Ctrl+C` in the terminal to stop it.

## Database

The app creates `tasks.db` automatically in the project folder when it starts. Do not delete it if you want to keep your tasks. The database file is local to your computer.

## Project structure

```text
Student_Task_Manager/
├── app.py
├── requirements.txt
├── README.md
├── tasks.db             # generated automatically when app runs
├── templates/
│   ├── index.html
│   ├── edit.html
│   └── 404.html
└── static/
    └── style.css
```

## Before deployment

This is designed as a local learning project. Before publishing it publicly, set a strong secret key through an environment variable, turn off Flask debug mode, and use a production WSGI server.
