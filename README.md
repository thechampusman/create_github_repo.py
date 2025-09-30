# create_github_repo.py

A tiny, focused CLI helper to bootstrap a new Git repository and push the first commit to a remote (for example, GitHub).

This script initializes a local git repository, creates a minimal `README.md` using the current folder name as the project title, makes the initial commit, renames the default branch to `main`, adds the remote `origin`, and pushes the commit upstream.

Why this exists
- Saves the repetitive steps when creating a new project and pushing it to a remote for the first time.
- Useful when you want a quick one-command bootstrap after creating an empty remote repository on GitHub (or another Git host).

Features
- Interactive prompt for the remote repository URL (supports HTTPS and SSH remotes).
- Creates a simple `README.md` titled with your current folder name.
- Runs `git init`, `git add`, `git commit`, renames the branch to `main`, sets `origin`, and pushes the initial commit.

Prerequisites
- Python 3.x installed and available on your PATH.
- Git installed and available on your PATH.
- A remote repository already created (for example on GitHub). You can use an HTTPS URL or an SSH URL (e.g. `https://github.com/user/repo.git` or `git@github.com:user/repo.git`).
- Authentication set up for the remote (SSH keys for `git@` URLs, or cached credentials / PAT for HTTPS pushes).

Quick start (PowerShell)

1. Open a terminal in your project folder (the folder name becomes the README title).
2. Run the script and follow the prompt:

```powershell
python .\create_github_repo.py
```

3. When asked, paste the remote repository URL and press Enter. The script will run the git commands and push the initial commit.

Example session

```
Enter remote repository URL (https or git@): https://github.com/youruser/yourrepo.git
$ git init
$ git add README.md
$ git commit -m "first commit"
$ git branch -M main
$ git remote add origin https://github.com/youruser/yourrepo.git
$ git push -u origin main
Done.
```

Notes & troubleshooting
- If `git push` fails, check that the remote repository exists and that your authentication is configured correctly (SSH keys or Personal Access Token for HTTPS).
- Ensure your global git config has a user name and email set, e.g. `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`.
- The script is intentionally small and interactive. If you need non-interactive behavior or extra options (custom commit message, skipping README creation, different branch name), consider forking and extending the script.

Contributing
- Small cleanups and improvements are welcome. If you add features, please include usage examples and tests where appropriate.

License
- No license file is included in this repository. Add a LICENSE if you want to make the project's license explicit.

Enjoy! If you'd like, I can add command-line options (for non-interactive usage), a unit test for the README writer, or an optional --title flag to override the folder name.