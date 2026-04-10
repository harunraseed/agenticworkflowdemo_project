# Setup Guide

## Prerequisites

Before starting, make sure you have:

- **Python 3.9+** installed — [Download Python](https://www.python.org/downloads/)
- **Git** installed — [Download Git](https://git-scm.com/)
- **GitHub account** with Copilot access
- **GitHub CLI** v2.0.0+ — [Download GitHub CLI](https://cli.github.com/)

## Step 1: Clone and Run the Demo App

```bash
# Clone the repository
git clone <your-repo-url>
cd agentic_workflows

# Set up Python virtual environment
cd app
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open your browser to **http://localhost:5000** — you should see the Project Tracker dashboard.

## Step 2: Run the Tests

```bash
cd app
python test_app.py
```

You should see all tests pass:
```
🧪 Running Project Tracker Tests

  ✅ GET /api/projects — returned 4 projects
  ✅ GET /api/projects/1 — got AI Chatbot
  ✅ GET /api/projects/999 — correctly returned 404
  ✅ POST /api/projects — created project id 5
  ✅ POST /api/projects (invalid) — correctly returned 400
  ✅ GET /api/stats — total: 5 | overdue: 0
  ✅ GET / — homepage loaded successfully

🎉 All tests passed!
```

## Step 3: Install the Agentic Workflows CLI

```bash
# Make sure GitHub CLI is installed and authenticated
gh auth login

# Install the Agentic Workflows extension
gh extension install github/gh-aw

# Verify installation
gh aw --help
```

## Step 4: Initialize Agentic Workflows

```bash
# Navigate to the repo root
cd agentic_workflows

# Initialize (creates necessary config)
gh aw init

# Compile the agent markdown files into GitHub Actions YAML
gh aw compile .github/agents/issue-triage.md
gh aw compile .github/agents/pr-reviewer.md
gh aw compile .github/agents/daily-status.md
```

## Step 5: Push to GitHub and Watch It Work

```bash
# Create a GitHub repo and push
gh repo create student-project-tracker --public --source=. --push

# Now open an issue to trigger the Issue Triage agent!
gh issue create --title "App crashes when adding project without due date" \
  --body "When I try to add a new project and leave the due date empty, the app shows an error."
```

Within seconds, the Issue Triage agent will:
1. Read your issue
2. Classify it as a **bug**
3. Add labels: `bug`, `priority: medium`
4. Post a comment asking for more details

## Project Structure

```
agentic_workflows/
├── app/
│   ├── app.py                    # Flask web app (Python)
│   ├── test_app.py               # Automated tests
│   ├── requirements.txt          # Python dependencies
│   └── templates/
│       └── index.html            # Dashboard UI
├── .github/
│   ├── agents/                   # Agentic Workflow sources (Markdown)
│   │   ├── issue-triage.md       # AI issue classification agent
│   │   ├── pr-reviewer.md        # AI code review agent
│   │   └── daily-status.md       # AI daily health report agent
│   └── workflows/                # Compiled GitHub Actions (YAML)
│       ├── ci.yml                # Traditional CI (tests & lint)
│       ├── issue-triage.yml      # Compiled from issue-triage.md
│       ├── pr-reviewer.yml       # Compiled from pr-reviewer.md
│       └── daily-status.yml      # Compiled from daily-status.md
├── docs/
│   ├── SETUP_GUIDE.md            # This file
│   ├── PRESENTATION_GUIDE.md     # How to present the demo
│   └── AGENTIC_WORKFLOWS_EXPLAINED.md  # Deep explanation
└── README.md
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` command not found | Try `python3` instead, or add Python to PATH |
| `gh` command not found | Install GitHub CLI from https://cli.github.com/ |
| `gh aw` not recognized | Run `gh extension install github/gh-aw` |
| Flask app won't start | Make sure you activated the virtual environment |
| Port 5000 already in use | Change port: `python app.py` and edit `app.run(port=5001)` |
