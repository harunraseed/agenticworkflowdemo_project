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


def test_search_by_name():
    """Test searching projects by name."""
    client = app.test_client()
    response = client.get("/api/projects?search=AI")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) >= 1
    assert all("ai" in p["title"].lower() or "ai" in p.get("description", "").lower() for p in data)
    print("  ✅ GET /api/projects?search=AI — returned", len(data), "project(s)")


def test_search_by_description():
    """Test searching projects by description."""
    client = app.test_client()
    response = client.get("/api/projects?search=visualization")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) >= 1
    assert any("visualization" in p.get("description", "").lower() for p in data)
    print("  ✅ GET /api/projects?search=visualization — returned", len(data), "project(s)")


def test_search_case_insensitive():
    """Test that search is case-insensitive."""
    client = app.test_client()
    response_lower = client.get("/api/projects?search=chatbot")
    response_upper = client.get("/api/projects?search=CHATBOT")

    data_lower = json.loads(response_lower.data)
    data_upper = json.loads(response_upper.data)

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    assert len(data_lower) == len(data_upper)
    print("  ✅ Search is case-insensitive — 'chatbot' and 'CHATBOT' return same count")


def test_search_no_results():
    """Test search that returns no results."""
    client = app.test_client()
    response = client.get("/api/projects?search=xyznonexistentproject")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == []
    print("  ✅ GET /api/projects?search=xyznonexistentproject — correctly returned empty list")


def test_search_empty_query():
    """Test that an empty search returns all projects."""
    client = app.test_client()
    all_response = client.get("/api/projects")
    search_response = client.get("/api/projects?search=")

    all_data = json.loads(all_response.data)
    search_data = json.loads(search_response.data)

    assert search_response.status_code == 200
    assert len(search_data) == len(all_data)
    print("  ✅ GET /api/projects?search= — empty query returns all", len(search_data), "projects")


if __name__ == "__main__":
    print("\n🧪 Running Student Project Tracker Tests\n")
    test_get_projects()
    test_get_single_project()
    test_project_not_found()
    test_create_project()
    test_create_project_validation()
    test_get_stats()
    test_homepage()
    test_search_by_name()
    test_search_by_description()
    test_search_case_insensitive()
    test_search_no_results()
    test_search_empty_query()
    print("\n🎉 All tests passed!\n")
