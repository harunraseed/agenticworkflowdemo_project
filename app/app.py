"""
Student Project Tracker - A simple Flask app to demonstrate GitHub Agentic Workflows.

This app lets students track their team projects. It's intentionally simple so the
focus stays on the agentic workflows (CI/CD automation with AI) rather than the app itself.
"""

from flask import Flask, jsonify, request, render_template
from datetime import datetime
import os

# Resolve the templates folder relative to this file so it works both
# locally (python app.py) and on Vercel (imported from api/index.py).
_base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(_base_dir, "templates"))

# ──────────────────────────────────────────────
# In-memory data store (no database needed for demo)
# ──────────────────────────────────────────────
projects = [
    {
        "id": 1,
        "title": "AI Chatbot",
        "description": "Build a chatbot using OpenAI API that helps students with homework",
        "team": "Team Alpha",
        "status": "in-progress",
        "priority": "high",
        "created_at": "2026-03-01",
        "due_date": "2026-04-15",
    },
    {
        "id": 2,
        "title": "Weather Dashboard",
        "description": "Real-time weather dashboard with data visualization using Matplotlib",
        "team": "Team Beta",
        "status": "planning",
        "priority": "medium",
        "created_at": "2026-03-10",
        "due_date": "2026-04-30",
    },
    {
        "id": 3,
        "title": "Student Portal",
        "description": "Portal for managing student grades and attendance records",
        "team": "Team Gamma",
        "status": "completed",
        "priority": "high",
        "created_at": "2026-02-15",
        "due_date": "2026-03-20",
    },
    {
        "id": 4,
        "title": "Campus Navigator",
        "description": "Mobile-friendly map app to help new students navigate campus",
        "team": "Team Delta",
        "status": "planning",
        "priority": "low",
        "created_at": "2026-03-20",
        "due_date": "2026-05-10",
    },
]

next_id = 5


# ──────────────────────────────────────────────
# Web Pages
# ──────────────────────────────────────────────
@app.route("/")
def index():
    """Serve the main dashboard page."""
    return render_template("index.html")


# ──────────────────────────────────────────────
# REST API Endpoints
# ──────────────────────────────────────────────
def filter_projects(query):
    """Return projects whose title or description contain the query (case-insensitive)."""
    q = query.lower()
    return [
        p for p in projects
        if q in p["title"].lower() or q in p.get("description", "").lower()
    ]


@app.route("/api/projects", methods=["GET"])
def get_projects():
    """Return all projects, optionally filtered by a search query.

    Query parameters:
        search (str): Case-insensitive substring to match against title or description.
    """
    search = request.args.get("search", "").strip()
    result = filter_projects(search) if search else projects
    return jsonify(result)


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Return a single project by ID."""
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)


@app.route("/api/projects", methods=["POST"])
def create_project():
    """Create a new project."""
    global next_id
    data = request.get_json()

    if not data or not data.get("title") or not data.get("team"):
        return jsonify({"error": "Title and team are required"}), 400

    project = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "team": data["team"],
        "status": data.get("status", "planning"),
        "priority": data.get("priority", "medium"),
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "due_date": data.get("due_date", ""),
    }
    next_id += 1
    projects.append(project)
    return jsonify(project), 201


@app.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    """Update an existing project."""
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json()
    for key in ["title", "description", "team", "status", "priority", "due_date"]:
        if key in data:
            project[key] = data[key]

    return jsonify(project)


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project."""
    global projects
    original_len = len(projects)
    projects = [p for p in projects if p["id"] != project_id]
    if len(projects) == original_len:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Project deleted"})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return dashboard statistics."""
    today = datetime.now().strftime("%Y-%m-%d")
    stats = {
        "total": len(projects),
        "by_status": {
            "planning": sum(1 for p in projects if p["status"] == "planning"),
            "in-progress": sum(1 for p in projects if p["status"] == "in-progress"),
            "completed": sum(1 for p in projects if p["status"] == "completed"),
        },
        "by_priority": {
            "high": sum(1 for p in projects if p["priority"] == "high"),
            "medium": sum(1 for p in projects if p["priority"] == "medium"),
            "low": sum(1 for p in projects if p["priority"] == "low"),
        },
        "overdue": sum(
            1
            for p in projects
            if p["due_date"] and p["due_date"] < today and p["status"] != "completed"
        ),
    }
    return jsonify(stats)


# ──────────────────────────────────────────────
# Run the app
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Student Project Tracker running at http://localhost:5000")
    app.run(debug=True, port=5000)
