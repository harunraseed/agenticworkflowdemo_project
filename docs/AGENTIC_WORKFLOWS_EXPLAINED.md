# GitHub Agentic Workflows — Explained for Students

## TL;DR

**Agentic Workflows = AI agents that live inside your CI/CD pipeline and act autonomously.**

Instead of writing rigid automation rules, you write natural language instructions in a Markdown file. An AI agent reads your repo, understands context, makes decisions, and takes action — all within GitHub Actions.

---

## 1. The Problem: Traditional CI/CD is Dumb (But Reliable)

Traditional GitHub Actions are like a **vending machine**:
- You press a button (push code, open a PR)
- It runs the exact same steps every time
- It has ZERO understanding of *what* your code does

Example of a typical workflow:
```yaml
on: push
jobs:
  test:
    steps:
      - run: python -m pytest    # Always runs the same tests
      - run: flake8 .            # Always checks the same rules
```

This is **deterministic** — great for reliability, but it can't:
- Read an issue and decide if it's a bug or feature request
- Look at a PR and explain what it does in plain English
- Notice that your repo has stale issues that need attention

---

## 2. The Solution: Add Intelligence to CI/CD

Agentic Workflows add an **AI reasoning layer** on top of GitHub Actions:

```
┌─────────────────────────────────────────────┐
│          GitHub Agentic Workflows           │
│                                             │
│   ┌─────────┐    ┌──────────┐    ┌──────┐  │
│   │ Trigger │───▶│ AI Agent │───▶│ Act  │  │
│   │ (Event) │    │ (Reason) │    │(Safe)│  │
│   └─────────┘    └──────────┘    └──────┘  │
│                                             │
│   Issue opened    Reads context   Adds label│
│   PR created      Makes decision  Comments  │
│   Schedule        Analyzes code   Reviews   │
└─────────────────────────────────────────────┘
```

---

## 3. How It Works (Step by Step)

### Step 1: Write a Markdown File

You create a `.md` file in `.github/agents/` with two parts:

**Frontmatter** (YAML at the top) — defines WHEN it runs and WHAT it can access:
```yaml
---
on: issues.opened          # Trigger: when an issue is opened
permissions:
  issues: write            # Can write to issues
  contents: read           # Can read repo contents
safe-outputs:
  - type: issue-comment    # Allowed action: post a comment
  - type: issue-label      # Allowed action: add a label
---
```

**Body** (Markdown below) — natural language instructions for the AI agent:
```markdown
# Issue Triage Agent

When a new issue is opened:
1. Read the title and description
2. Classify it as bug, feature, or question
3. Add the appropriate label
4. Post a friendly comment explaining your classification
```

### Step 2: Compile It

Run `gh aw compile .github/agents/issue-triage.md`

This transforms your Markdown into a standard GitHub Actions YAML file. The compiled file goes into `.github/workflows/`.

### Step 3: It Runs Automatically

When someone opens an issue, GitHub Actions triggers the workflow. The AI agent:
1. **Reads** the issue content and repo context
2. **Reasons** about what kind of issue it is
3. **Acts** by adding labels and posting a comment

All within the secure sandbox of GitHub Actions.

---

## 4. Why Is This Secure?

Great question! Letting AI take actions sounds scary. Here's how it's locked down:

```
┌──────────────────────────────────────────────┐
│              Security Architecture            │
│                                              │
│  1. Agent runs READ-ONLY by default          │
│     ↓                                        │
│  2. Agent PROPOSES actions                   │
│     ↓                                        │
│  3. Threat detection SCANS proposals         │
│     ↓                                        │
│  4. Safe actions execute in ISOLATED sandbox │
│                                              │
│  The agent NEVER has direct write access!    │
└──────────────────────────────────────────────┘
```

- **Read-only default**: The agent can look at everything but touch nothing
- **Safe outputs**: You explicitly declare what actions are allowed (e.g., "can only add comments")
- **Threat detection**: Every proposed action is scanned before execution
- **Isolated containers**: Actions run in sandboxes that can't affect the rest of the system

---

## 5. Agentic Workflows vs Regular GitHub Actions

| Aspect | GitHub Actions (Traditional) | Agentic Workflows |
|--------|------------------------------|-------------------|
| **Logic** | Rigid YAML rules | Natural language instructions |
| **Decision Making** | If/else conditions | AI reasoning with context |
| **Adaptability** | Same behavior every time | Adapts to each situation |
| **Understanding** | None — just runs commands | Reads and understands content |
| **Setup** | Write YAML | Write Markdown + compile |
| **Security** | Permissions-based | Permissions + threat detection + sandbox |
| **Use Cases** | Build, test, deploy | Triage, review, report, govern |

---

## 6. The Evolution Timeline

```
2019 ─── GitHub Actions ──────── "Run this script when code is pushed"
  │       Deterministic automation. No intelligence.
  │
2021 ─── GitHub Copilot ─────── "Help me write this function"
  │       AI assists in the editor. Human stays in control.
  │
2025 ─── Coding Agent ──────── "Implement this feature across files"
  │       AI works on tasks. Goal-driven. Still bounded.
  │
2025 ─── Agentic Workflows ── "Monitor, reason, and act 24/7"
          AI embedded in CI/CD. Continuous intelligence.
```

---

## 7. Real-World Use Cases

### For a Student Project Like Ours:

| Workflow | What It Does | When It Runs |
|----------|-------------|-------------|
| **Issue Triage** | Auto-labels issues as bug/feature/question, asks for missing info | Every new issue |
| **PR Reviewer** | Summarizes code changes, checks for bugs, suggests improvements | Every new PR |
| **Daily Status** | Generates a health report with stats, risks, recommendations | Every morning |

### For Companies & Organizations:

- **Dependabot Config Rollout** — Automatically configure dependency scanning across 100+ repos
- **License Compliance** — Check that every PR respects open-source license rules
- **Release Notes** — Auto-generate changelog from PR descriptions
- **Onboarding** — Detect a new contributor's first PR and provide helpful guidance
- **Stale Cleanup** — Intelligently close old issues that are no longer relevant

---

## 8. Key Concepts Glossary

| Term | Meaning |
|------|---------|
| **Agentic Workflow** | A GitHub Actions workflow powered by an AI agent |
| **Frontmatter** | The YAML config at the top of the Markdown source file |
| **Safe Outputs** | Explicitly declared actions the agent is allowed to take |
| **Compile** | Transform Markdown source → GitHub Actions YAML |
| **Continuous AI** | The vision of AI running continuously in your dev lifecycle |
| **gh aw** | The CLI tool to manage agentic workflows |
| **Agentics Collection** | GitHub's library of pre-built agentic workflow templates |
| **Deterministic** | Same input → always same output (traditional CI/CD) |
| **Probabilistic** | AI reasoning — intelligent but not 100% predictable |

---

## 9. Getting Started Yourself

```bash
# 1. Install GitHub CLI (if you don't have it)
#    Download from: https://cli.github.com/

# 2. Verify version (need 2.0.0+)
gh --version

# 3. Install the Agentic Workflows extension
gh extension install github/gh-aw

# 4. Navigate to your repo
cd my-project

# 5. Initialize agentic workflows
gh aw init

# 6. Add a pre-built workflow from the Agentics collection
gh aw add

# 7. Or compile your own custom workflow
gh aw compile .github/agents/my-workflow.md
```

---

## 10. Think About It

Traditional CI/CD answers: **"What should I DO when this event happens?"**

Agentic Workflows answer: **"What should I THINK about when this event happens, and what's the RIGHT thing to do?"**

That's the shift from *automation* to *intelligence*.

---

*This guide was created for the GitHub Copilot Dev Days workshop.*
