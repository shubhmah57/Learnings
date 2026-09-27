# Artificial Intelligence Learnings

This repository collects AI learning projects and exercises. Each project should live in its own subfolder so you can add multiple projects over time.

Current folders in this workspace:

- `udemy-ed-donner-ownpractice` — Udemy exercises and practice (current project).

How to add a new project:

1. Create a new folder at the repository root, e.g. `my-new-project/`.
2. Add your code, `README.md`, and (optionally) a `requirements.txt` or `pyproject.toml`.
3. Commit and push.

Recommended git workflow (from the repository root):

```powershell
git init
git add .
git commit -m "Initial import: udemy-ed-donner-ownpractice"
# Create remote and push (use gh or create repo on github.com)
# Using GitHub CLI:
gh repo create shubham9415/Artificial-Intelligence-Learnings --public --source=. --remote=origin --push
# Or create repo on github.com and then:
# git remote add origin https://github.com/shubham9415/Artificial-Intelligence-Learnings.git
# git branch -M main
# git push -u origin main
```

If you want, I can add a `.gitignore` and create the initial commit for you; you'll need to authenticate `gh` or provide credentials to push to GitHub.