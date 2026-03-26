"""
Simple tests for the Student Project Tracker API.
Run with: python test_app.py
"""

import json
from app import app


def test_get_projects():
    """Test listing all projects."""
    client = app.test_client()
    response = client.get("/api/projects")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) >= 3
    print("  ✅ GET /api/projects — returned", len(data), "projects")


def test_get_single_project():
    """Test fetching a single project."""
    client = app.test_client()
    response = client.get("/api/projects/1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["title"] == "AI Chatbot"
    print("  ✅ GET /api/projects/1 — got", data["title"])


def test_project_not_found():
    """Test 404 for non-existent project."""
    client = app.test_client()
    response = client.get("/api/projects/999")

    assert response.status_code == 404
    print("  ✅ GET /api/projects/999 — correctly returned 404")


def test_create_project():
    """Test creating a new project."""
    client = app.test_client()
    new_project = {
        "title": "Test Project",
        "team": "Team Test",
        "description": "A project created by automated tests",
        "priority": "low",
    }
    response = client.post(
        "/api/projects",
        data=json.dumps(new_project),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["title"] == "Test Project"
    assert data["status"] == "planning"  # default status
    print("  ✅ POST /api/projects — created project id", data["id"])


def test_create_project_validation():
    """Test that title and team are required."""
    client = app.test_client()
    response = client.post(
        "/api/projects",
        data=json.dumps({"description": "missing title and team"}),
        content_type="application/json",
    )

    assert response.status_code == 400
    print("  ✅ POST /api/projects (invalid) — correctly returned 400")


def test_get_stats():
    """Test the stats endpoint."""
    client = app.test_client()
    response = client.get("/api/stats")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "total" in data
    assert "by_status" in data
    assert "by_priority" in data
    assert "overdue" in data
    print("  ✅ GET /api/stats — total:", data["total"], "| overdue:", data["overdue"])


def test_homepage():
    """Test that the homepage loads."""
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Student Project Tracker" in response.data
    print("  ✅ GET / — homepage loaded successfully")


if __name__ == "__main__":
    print("\n🧪 Running Student Project Tracker Tests\n")
    test_get_projects()
    test_get_single_project()
    test_project_not_found()
    test_create_project()
    test_create_project_validation()
    test_get_stats()
    test_homepage()
    print("\n🎉 All tests passed!\n")
