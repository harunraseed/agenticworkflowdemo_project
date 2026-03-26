# Presentation Guide — GitHub Agentic Workflows Demo

## Audience

College students, likely with:
- Basic Python knowledge
- Some Git/GitHub experience
- Little or no CI/CD experience
- Curiosity about AI in software development

## Timing: ~30 Minutes

| Time | Section | Duration |
|------|---------|----------|
| 0:00 | Introduction & Hook | 3 min |
| 0:03 | Evolution of CI/CD (The Journey) | 5 min |
| 0:08 | What Are Agentic Workflows? | 5 min |
| 0:13 | Demo 1: The App + Traditional CI | 5 min |
| 0:18 | Demo 2: Agentic Workflows in Action | 7 min |
| 0:25 | Wrap-up & Q&A | 5 min |

---

## Section 1: Introduction & Hook (3 min)

### Opening Question (Get Engagement!)

> "How many of you have ever opened a GitHub issue or pull request?"
> (Show of hands)
>
> "Now — how many of you have ever WISHED someone would automatically read your issue,
> figure out if it's a bug or feature request, label it, and respond to you instantly?"
>
> "That's exactly what we're going to build today."

### Set the Stage

- We're going to take a simple Python web app
- Add AI agents that LIVE inside the CI/CD pipeline
- These agents will *understand* code, *reason* about issues, and *act* autonomously
- All secured, auditable, and within GitHub Actions

---

## Section 2: The Evolution (5 min)

### Draw This on Whiteboard or Show Slide

```
2019: GitHub Actions     → "if push, run tests"           🔧 Automation
2021: GitHub Copilot     → "help me write this code"      🧑‍💻 AI-Assisted
2025: Coding Agent       → "implement this feature"       🤖 Task-Driven
2025: Agentic Workflows  → "monitor, reason, act 24/7"   🧠 Continuous AI
```

### Key Talking Point

> "The question isn't 'will AI change software development?' — it already has.
> The question is: 'Where does AI live in your development process?'
>
> - First it was in your editor (Copilot)
> - Then it could do whole tasks (Coding Agent)
> - Now it lives in your CI/CD — ALWAYS watching, ALWAYS reasoning"

---

## Section 3: What Are Agentic Workflows? (5 min)

### Show the Architecture

Open `.github/agents/issue-triage.md` and walk through:

1. **Frontmatter** = "the rules" — when does it run, what can it access
2. **Body** = "the brain" — natural language instructions for the AI

### Key Contrast

> "In traditional CI/CD, you write: `if label == 'bug': assign_to('dev-team')`
>
> In Agentic Workflows, you write: 'Read this issue. Figure out if it's a bug. If it is, add the bug label and ask for reproduction steps.'"

### Security Slide

Emphasize the 3-layer security model:
1. Agent is **read-only** by default
2. Proposed actions go through **threat detection**
3. Execution happens in **isolated containers**

> "The AI can THINK about anything, but it can only DO what you explicitly allow."

---

## Section 4: Demo 1 — The App + Traditional CI (5 min)

### Run the Flask App

```bash
cd app
python app.py
```

**Show the browser** at http://localhost:5000:
- Walk through the dashboard (stats cards, project list)
- Add a new project live
- Show this is a real, working Python application

### Show Traditional CI

Open `.github/workflows/ci.yml`:

> "This is what most of you are familiar with — traditional CI.
> Push code → run tests → pass or fail. It's deterministic.
> It has NO idea what your code does. It just runs commands."

---

## Section 5: Demo 2 — Agentic Workflows in Action (7 min)

### Demo 2a: Issue Triage Agent

1. **Show the source**: Open `.github/agents/issue-triage.md`
   - Point out frontmatter (trigger, permissions, safe-outputs)
   - Point out the natural language instructions

2. **Show the compiled output**: Open `.github/workflows/issue-triage.yml`
   - "This Markdown gets compiled into a standard GitHub Action"
   - "The magic: the AI agent step reads context and makes decisions"

3. **Simulate**: Open a GitHub issue on the repo:
   ```
   Title: "App crashes when I add a project without a due date"
   Body: "I filled in the title and team but left due date empty. When I click Add, nothing happens."
   ```

4. **Show the result**: The agent comments with classification (bug), adds labels, asks for details

### Demo 2b: PR Reviewer Agent

1. **Show the source**: Open `.github/agents/pr-reviewer.md`
2. **Create a small code change** (e.g., add a search endpoint to `app.py`)
3. **Open a PR**: The agent reviews the code, summarizes changes, suggests improvements

### Demo 2c: Daily Status Report

1. **Show the source**: Open `.github/agents/daily-status.md`
2. **Explain**: "This runs every morning at 9 AM and creates a health report issue"
3. **Show the template**: Walk through what the report looks like

### The "Aha!" Moment

> "Notice what just happened:
> - The issue triage agent READ the issue and UNDERSTOOD it was a bug
> - The PR reviewer READ the diff and EXPLAINED what changed
> - The daily status agent ANALYZES the whole repo and GENERATES insights
>
> None of this is hardcoded. The AI REASONS about each situation differently."

---

## Section 6: Wrap-up & Q&A (5 min)

### Three Takeaways

1. **Agentic Workflows = AI inside CI/CD** — not a separate tool, built into what teams already use
2. **Write Markdown, not YAML** — instructions are natural language, making automation accessible
3. **Secure by design** — read-only agents, threat detection, sandboxed execution

### Call to Action

> "Want to try it yourself? Here's all you need:"
>
> ```bash
> gh extension install github/gh-aw
> gh aw init
> gh aw add   # Pick from pre-built templates
> ```
>
> "Check out the Agentics Collection on GitHub for real-world examples."

### Common Student Questions (Be Ready!)

| Question | Answer |
|----------|--------|
| "Can I use this for free?" | GitHub Copilot is needed. Check if your school has GitHub Education access. |
| "Is this like ChatGPT?" | Similar AI, but it LIVES in your CI/CD and acts autonomously on repo events. |
| "Can the AI break my code?" | No — it runs read-only with sandboxed execution. It can only do what you allow. |
| "What languages does it support?" | Any! The AI understands all major programming languages. |
| "Can I use it for my class project?" | Absolutely — that's the perfect place to start. |
| "How is this different from Copilot?" | Copilot helps you CODE. Agentic Workflows help you AUTOMATE with intelligence. |

---

## Demo Tips

- **Pre-create the GitHub repo** before the session to save time
- **Have issues pre-created** so you can show triage results instantly
- **Use VS Code** to show the Markdown and YAML files side by side
- **Keep a terminal open** with the Flask app running
- **Have the GitHub repo open in a browser tab** to show Actions running
- **Practice the demos 2-3 times** to get smooth transitions

---

## Files to Have Open During Demo

1. Browser: `http://localhost:5000` (the app)
2. Browser: GitHub repo → Actions tab
3. VS Code: `.github/agents/issue-triage.md`
4. VS Code: `.github/workflows/issue-triage.yml` (side by side)
5. Terminal: Flask app running

Good luck with your presentation! 🎉
