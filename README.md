# GitHub Agentic Workflows — Demo Project

## Student Project Tracker with AI-Powered CI/CD

This demo project showcases **GitHub Agentic Workflows** — AI agents that live inside your CI/CD pipeline and continuously observe, reason, and act on your repository.

Built for **GitHub Copilot Dev Days** — designed to be presented to college students.

---

### What's Inside

```
agentic_workflows/
├── app/                              # Python Flask web app
│   ├── app.py                        # Main application (REST API + web UI)
│   ├── test_app.py                   # Automated tests
│   ├── requirements.txt              # Python dependencies (Flask)
│   └── templates/
│       └── index.html                # Dashboard UI (HTML/CSS/JS)
├── .github/
│   ├── agents/                       # Agentic Workflow sources (Markdown)
│   │   ├── issue-triage.md           # AI auto-triage for new issues
│   │   ├── pr-reviewer.md            # AI code review for pull requests
│   │   └── daily-status.md           # AI daily repository health report
│   └── workflows/                    # Compiled GitHub Actions (YAML)
│       ├── ci.yml                    # Traditional CI (tests — for comparison)
│       ├── issue-triage.yml          # Compiled from issue-triage.md
│       ├── pr-reviewer.yml           # Compiled from pr-reviewer.md
│       └── daily-status.yml          # Compiled from daily-status.md
├── docs/
│   ├── SETUP_GUIDE.md                # Step-by-step setup instructions
│   ├── PRESENTATION_GUIDE.md         # How to present this demo (30 min)
│   └── AGENTIC_WORKFLOWS_EXPLAINED.md  # Deep explanation for students
├── .gitignore
└── README.md                         # This file
```

---

### Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/)
- **GitHub account** with Copilot access
- **GitHub CLI** v2.0.0+ — [Download](https://cli.github.com/)

---

### Quick Start

```bash
# 1. Clone this repo
git clone <your-repo-url>
cd agentic_workflows

# 2. Run the demo app
cd app
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python app.py                  # Open http://localhost:5000

# 3. Run tests
python test_app.py

# 4. Install the Agentic Workflows CLI
gh extension install github/gh-aw

# 5. Initialize & compile
gh aw init
gh aw compile .github/agents/issue-triage.md
gh aw compile .github/agents/pr-reviewer.md
gh aw compile .github/agents/daily-status.md
```

---

### Demo Scenarios

| Demo | What Happens | Trigger |
|------|-------------|---------|
| **Issue Triage** | AI reads new issues, classifies them (bug/feature/question), adds labels, responds | Open a new issue |
| **PR Reviewer** | AI reviews code changes, summarizes, checks for bugs, suggests improvements | Open a pull request |
| **Daily Status** | AI generates a daily health report with stats, risks, and recommendations | Scheduled (daily) or manual |

---

### The Evolution: Automation → Intelligence

```
2019: GitHub Actions    → "If push, run tests"         (Deterministic)
2021: GitHub Copilot    → "Help me write this code"     (AI-Assisted)
2025: Coding Agent      → "Implement this feature"      (Task-Driven AI)
2025: Agentic Workflows → "Monitor, reason, act 24/7"   (Continuous AI)
```

---

### Security Model

Agentic Workflows are secure by design:

1. **Read-Only Default** — Agent cannot modify anything directly
2. **Threat Detection** — All proposed actions are scanned before execution
3. **Isolated Execution** — Actions run in sandboxed containers
4. **Auditable** — Every decision and action is logged

---

### Documentation

| Document | Purpose |
|----------|---------|
| [Setup Guide](docs/SETUP_GUIDE.md) | Step-by-step installation and configuration |
| [Presentation Guide](docs/PRESENTATION_GUIDE.md) | 30-minute demo script with talking points |
| [Workflows Explained](docs/AGENTIC_WORKFLOWS_EXPLAINED.md) | Deep technical explanation for students |

---

Built for **GitHub Copilot Dev Days** demonstration
