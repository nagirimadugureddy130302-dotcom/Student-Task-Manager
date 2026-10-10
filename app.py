import sqlite3
from pathlib import Path
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).resolve().parent / "tasks.db"

PRIORITIES = {"Low", "Medium", "High"}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                due_date TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def task_is_overdue(task):
    return bool(task["due_date"]) and task["due_date"] < date.today().isoformat() and not task["completed"]


@app.template_filter("overdue")
def overdue_filter(task):
    return task_is_overdue(task)


@app.route("/")
def home():
    with get_db() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY completed ASC, "
            "CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, "
            "CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END, due_date ASC, id DESC"
        ).fetchall()
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["completed"])
        pending_tasks = total_tasks - completed_tasks

    progress = round(completed_tasks * 100 / total_tasks) if total_tasks else 0
    overdue_tasks = sum(1 for task in tasks if task_is_overdue(task))
    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        progress=progress,
        overdue_tasks=overdue_tasks,
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    due_date = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "Medium")

    if not title or not subject:
        flash("Task title and subject are required.", "error")
        return redirect(url_for("home"))
    if priority not in PRIORITIES:
        flash("Please choose a valid priority.", "error")
        return redirect(url_for("home"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO tasks (title, subject, due_date, priority) VALUES (?, ?, ?, ?)",
            (title, subject, due_date or None, priority),
        )
    flash("Task added successfully.", "success")
    return redirect(url_for("home"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    with get_db() as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            abort(404)

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            subject = request.form.get("subject", "").strip()
            due_date = request.form.get("due_date", "").strip()
            priority = request.form.get("priority", "Medium")

            if not title or not subject:
                flash("Task title and subject are required.", "error")
                return render_template("edit.html", task=task, today=date.today().isoformat())
            if priority not in PRIORITIES:
                flash("Please choose a valid priority.", "error")
                return render_template("edit.html", task=task, today=date.today().isoformat())

            conn.execute(
                "UPDATE tasks SET title = ?, subject = ?, due_date = ?, priority = ? WHERE id = ?",
                (title, subject, due_date or None, priority, task_id),
            )
            flash("Task updated successfully.", "success")
            return redirect(url_for("home"))

    return render_template("edit.html", task=task, today=date.today().isoformat())


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    with get_db() as conn:
        task = conn.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            abort(404)
        new_status = 0 if task["completed"] else 1
        conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
    flash("Task status updated.", "success")
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


init_db()

if __name__ == "__main__":
    app.run(debug=True)
