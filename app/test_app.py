"""
Simple tests for the Project Tracker API.
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
    assert b"Project Tracker" in response.data
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
    # Verify that the same projects are returned, not just the same count.
    ids_lower = sorted(p["id"] for p in data_lower)
    ids_upper = sorted(p["id"] for p in data_upper)
    assert ids_lower == ids_upper
    print("  ✅ Search is case-insensitive — 'chatbot' and 'CHATBOT' return same projects")


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


def test_contact_page_loads():
    """Test that the Contact Us page loads successfully."""
    client = app.test_client()
    response = client.get("/contact")

    assert response.status_code == 200
    assert b"Contact Us" in response.data
    print("  ✅ GET /contact — Contact Us page loaded successfully")


def test_contact_page_has_form_fields():
    """Test that the Contact Us page contains all required form fields with correct attributes."""
    client = app.test_client()
    response = client.get("/contact")

    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Contact form element present
    assert '<form id="contact-form"' in html

    # Full Name: text input with id, name, and required
    assert 'id="c-name"' in html
    assert 'name="name"' in html

    # Email Address: email input with id and name
    assert 'id="c-email"' in html
    assert 'name="email"' in html
    assert 'type="email"' in html

    # Phone Number: tel input with id and name
    assert 'id="c-phone"' in html
    assert 'name="phone"' in html
    assert 'type="tel"' in html

    # Message: textarea element with id and name
    assert '<textarea' in html
    assert 'id="c-message"' in html
    assert 'name="message"' in html

    print("  ✅ GET /contact — all required form fields present (name, email, phone, message)")


def test_contact_page_has_submit_button():
    """Test that the Contact Us page contains a submit button."""
    client = app.test_client()
    response = client.get("/contact")

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'type="submit"' in html
    assert 'class="btn-submit"' in html
    print("  ✅ GET /contact — submit button present")


# ──────────────────────────────────────────────
# Team Registration Tests
# ──────────────────────────────────────────────

def test_register_page_loads():
    """Test that the team registration page loads."""
    client = app.test_client()
    response = client.get("/register")

    assert response.status_code == 200
    assert b"Team Registration" in response.data
    print("  ✅ GET /register — page loaded successfully")


def test_register_page_has_form_fields():
    """Test that the registration page contains all required fields."""
    client = app.test_client()
    response = client.get("/register")

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'id="r-team-name"' in html
    assert 'id="r-college"' in html
    assert 'id="r-email"' in html
    assert 'id="r-project-area"' in html
    assert 'id="members-list"' in html
    print("  ✅ GET /register — all required form fields present")


def test_get_teams_empty():
    """Test that GET /api/teams returns an empty list initially."""
    client = app.test_client()
    response = client.get("/api/teams")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, list)
    print("  ✅ GET /api/teams — returned list of", len(data), "team(s)")


def test_register_team():
    """Test registering a new team."""
    client = app.test_client()
    payload = {
        "team_name": "Test Rockets",
        "college_name": "Test University",
        "contact_email": "rockets@test.edu",
        "project_area": "Machine Learning",
        "members": ["Alice Smith", "Bob Jones", "Carol White"],
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["team_name"] == "Test Rockets"
    assert data["college_name"] == "Test University"
    assert data["contact_email"] == "rockets@test.edu"
    assert data["project_area"] == "Machine Learning"
    assert data["members"] == ["Alice Smith", "Bob Jones", "Carol White"]
    assert "id" in data
    assert "registered_at" in data
    print("  ✅ POST /api/teams — registered team id", data["id"])


def test_register_team_appears_in_list():
    """Test that a registered team shows up in GET /api/teams."""
    client = app.test_client()
    payload = {
        "team_name": "Visible Team",
        "college_name": "State College",
        "members": ["Dana Lee"],
    }
    client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )
    response = client.get("/api/teams")
    data = json.loads(response.data)

    assert response.status_code == 200
    names = [t["team_name"] for t in data]
    assert "Visible Team" in names
    print("  ✅ GET /api/teams — registered team appears in list")


def test_register_team_missing_team_name():
    """Test that missing team_name returns 400."""
    client = app.test_client()
    payload = {
        "college_name": "Test University",
        "members": ["Alice Smith"],
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    print("  ✅ POST /api/teams (no team_name) — correctly returned 400")


def test_register_team_missing_college_name():
    """Test that missing college_name returns 400."""
    client = app.test_client()
    payload = {
        "team_name": "No College Team",
        "members": ["Alice Smith"],
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    print("  ✅ POST /api/teams (no college_name) — correctly returned 400")


def test_register_team_missing_members():
    """Test that an empty members list returns 400."""
    client = app.test_client()
    payload = {
        "team_name": "Empty Team",
        "college_name": "Test University",
        "members": [],
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    print("  ✅ POST /api/teams (no members) — correctly returned 400")


def test_register_team_too_many_members():
    """Test that more than 5 members returns 400."""
    client = app.test_client()
    payload = {
        "team_name": "Huge Team",
        "college_name": "Big University",
        "members": ["A", "B", "C", "D", "E", "F"],  # 6 members
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    print("  ✅ POST /api/teams (6 members) — correctly returned 400")


def test_register_team_max_five_members():
    """Test that exactly 5 members is allowed."""
    client = app.test_client()
    payload = {
        "team_name": "Full Team",
        "college_name": "Five College",
        "members": ["A", "B", "C", "D", "E"],
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert len(data["members"]) == 5
    print("  ✅ POST /api/teams (5 members) — allowed, id", data["id"])


def test_register_team_no_body():
    """Test that a request with no JSON body returns 400."""
    client = app.test_client()
    response = client.post("/api/teams", content_type="application/json")

    assert response.status_code == 400
    print("  ✅ POST /api/teams (no body) — correctly returned 400")


if __name__ == "__main__":
    print("\n🧪 Running Project Tracker Tests\n")
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
    test_contact_page_loads()
    test_contact_page_has_form_fields()
    test_contact_page_has_submit_button()
    test_register_page_loads()
    test_register_page_has_form_fields()
    test_get_teams_empty()
    test_register_team()
    test_register_team_appears_in_list()
    test_register_team_missing_team_name()
    test_register_team_missing_college_name()
    test_register_team_missing_members()
    test_register_team_too_many_members()
    test_register_team_max_five_members()
    test_register_team_no_body()
    print("\n🎉 All tests passed!\n")
