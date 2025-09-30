import os
import subprocess


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
    url = input("Enter remote repository URL (https or git@): ").strip()
    if not url:
        print("No URL provided. Exiting.")
        exit(1)
    folder = os.path.basename(os.getcwd())
    readme = "README.md"
    content = f"# {folder}\n\nThis repository was initialized by create_github_repo.py.\n"
    create_readme(readme, content)
    run_cmd(["git", "init"])
    run_cmd(["git", "add", readme])
    run_cmd(["git", "commit", "-m", "first commit"])
    run_cmd(["git", "branch", "-M", "main"])
    run_cmd(["git", "remote", "add", "origin", url])
    run_cmd(["git", "push", "-u", "origin", "main"])
    print("Done.")


if __name__ == "__main__":
    main()
