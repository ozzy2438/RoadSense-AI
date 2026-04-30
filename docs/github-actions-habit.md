# GitHub Actions Habit Guide

This project is set up so every push teaches you something.

GitHub Actions is the robot checker for the repository. When you push code to GitHub, it reads files in `.github/workflows/` and runs the steps written there.

## The Habit Loop

Use this loop for every change, even small ones:

```bash
git status
# make one focused change
git status
git add <changed-files>
git commit -m "Short clear message"
git push
gh run list --limit 3
```

The habit is not "write perfect code first." The habit is:

1. Make one clear change.
2. Save it in Git with a commit.
3. Push it to GitHub.
4. Let GitHub Actions check it.
5. Fix the next clear thing.

## What Runs Today

The main workflow is `.github/workflows/ci.yml`.

It runs on every push and pull request:

| Job | What it checks |
| --- | --- |
| `python` | Installs the Python project, runs Ruff, runs tests, builds a small golden eval set, and runs the eval script. |
| `frontend` | Installs the Next.js console dependencies and runs a production build. |

If both jobs pass, the commit is healthy enough to continue from.

## How To Read A Failed Run

Use these commands:

```bash
gh run list --limit 5
gh run view <run-id> --log-failed
```

Read the first real error, not the last line. Most logs end with a summary, but the useful clue is usually earlier.

Common examples:

| Error type | Meaning | First move |
| --- | --- | --- |
| `ruff check` failed | Python style or import issue | Read the file and line number, then patch only that issue. |
| `pytest` failed | A test expectation is wrong or code behavior changed | Run the test locally and inspect the assertion. |
| `next build` failed | TypeScript or frontend build issue | Read the TypeScript error and fix the named component/file. |
| `npm audit` failed | Dependency vulnerability | Upgrade the direct package or add a safe override when appropriate. |

## Good Commit Messages

Use short messages that describe the step:

```text
Add GitHub Actions habit guide
Fix triage confidence threshold
Add prompt injection test case
Update frontend build dependencies
```

Avoid vague messages:

```text
update
changes
fix stuff
final
```

## Your Rule For This Repo

For RoadSense AI, treat every commit as a checkpoint:

```text
change -> commit -> push -> watch Actions -> continue
```

Small commits are good. They make mistakes easier to find and easier to fix.
