import os
import subprocess
import sys


def run_cmd(cmd):
    try:
        print(f"$ {' '.join(cmd)}")
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        print(f"Error running: {' '.join(cmd)}")
        exit(1)


def create_readme(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {path}")


def main():
    # Support optional CLI args: [target_folder] [remote_url]
    cli_folder = None
    cli_url = None
    if len(sys.argv) > 1:
        cli_folder = sys.argv[1]
    if len(sys.argv) > 2:
        cli_url = sys.argv[2]

    def choose_target_folder(arg=None):
        if arg:
            path = os.path.abspath(os.path.expanduser(arg))
        else:
            cur = os.getcwd()
            inp = input(f"Target folder for new repo (leave empty to use current folder: {cur}): ").strip()
            if not inp:
                return cur
            path = os.path.abspath(os.path.expanduser(inp))

        if not os.path.exists(path):
            create = input(f"Folder '{path}' does not exist. Create it? [y/N]: ").strip().lower()
            if create in ("y", "yes"):
                try:
                    os.makedirs(path, exist_ok=True)
                    print(f"Created folder: {path}")
                except OSError as e:
                    print(f"Failed to create folder: {e}")
                    exit(1)
            else:
                print("Aborting.")
                exit(1)

        gitdir = os.path.join(path, ".git")
        if os.path.isdir(gitdir):
            resp = input(f"Folder '{path}' already appears to be a git repository. Continue and use it? [y/N]: ").strip().lower()
            if resp not in ("y", "yes"):
                print("Aborting.")
                exit(1)

        return path

    target = choose_target_folder(cli_folder)
    os.chdir(target)

    url = cli_url or input("Enter remote repository URL (https or git@): ").strip()
    if not url:
        print("No URL provided. Exiting.")
        exit(1)

    folder = os.path.basename(os.path.abspath(os.getcwd()))
    readme = "README.md"
    content = f"# {folder}\n\nThis repository was initialized by create_github_repo.py.\n"
    create_readme(readme, content)

    # If .git already exists, skip git init
    if os.path.isdir(os.path.join(os.getcwd(), ".git")):
        print("Existing git repository detected. Skipping 'git init'.")
    else:
        run_cmd(["git", "init"])

    run_cmd(["git", "add", readme])
    run_cmd(["git", "commit", "-m", "first commit"])
    run_cmd(["git", "branch", "-M", "main"])
    run_cmd(["git", "remote", "add", "origin", url])
    run_cmd(["git", "push", "-u", "origin", "main"])
    print("Done.")


if __name__ == "__main__":
    main()
