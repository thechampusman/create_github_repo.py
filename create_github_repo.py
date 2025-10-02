import os
import subprocess
import sys


def run_cmd(cmd):
    try:
        print(f"$ {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        # Print the actual error output
        if e.stderr:
            print(e.stderr)
        
        # Check for specific git errors and provide helpful solutions
        error_text = (e.stderr or "") + (e.stdout or "")
        
        # Handle git commit specific errors
        if cmd[0] == "git" and len(cmd) > 1 and cmd[1] == "commit":
            if "nothing to commit" in error_text.lower():
                print("ℹ️  No changes to commit. This is normal if README.md already exists with the same content.")
                return None
            elif "please tell me who you are" in error_text.lower() or "user.email" in error_text.lower():
                print("\n⚠️  Git user configuration missing!")
                print("Git needs to know who you are for commits.")
                email = input("Enter your email for git commits: ").strip()
                name = input("Enter your name for git commits: ").strip()
                if email and name:
                    try:
                        subprocess.run(["git", "config", "--global", "user.email", email], check=True, capture_output=True)
                        subprocess.run(["git", "config", "--global", "user.name", name], check=True, capture_output=True)
                        print(f"✅ Git user configured: {name} <{email}>")
                        print("🔄 Retrying commit...")
                        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        if result.stdout:
                            print(result.stdout)
                        return result
                    except subprocess.CalledProcessError:
                        print("❌ Failed to configure git user.")
                else:
                    print("❌ Email and name are required for git commits.")
                    return None
        
        # Handle dubious ownership errors
        if cmd[0] == "git" and ("dubious ownership" in error_text.lower() or "safe.directory" in error_text.lower()):
            cwd = os.getcwd()
            print(f"\n🔒 Git Security Issue Detected!")
            print(f"Git has detected that the repository '{cwd}' has different ownership.")
            print("This is a security feature to prevent malicious code execution.")
            print("\nOptions to resolve this:")
            print("1. Add this directory to git safe directories (recommended)")
            print("2. Skip this operation and continue")
            print("3. Abort and exit")
            
            while True:
                choice = input("\nChoose an option [1/2/3]: ").strip()
                if choice == "1":
                    try:
                        print(f"\n🔧 Adding '{cwd}' to git safe directories...")
                        safe_cmd = ["git", "config", "--global", "--add", "safe.directory", cwd]
                        print(f"$ {' '.join(safe_cmd)}")
                        subprocess.run(safe_cmd, check=True, capture_output=True)
                        print("✅ Successfully added to safe directories!")
                        
                        print(f"🔄 Retrying original command...")
                        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        if result.stdout:
                            print(result.stdout)
                        print("✅ Command completed successfully!")
                        return result
                    except subprocess.CalledProcessError as retry_error:
                        print(f"❌ Failed to fix or retry: {retry_error}")
                        print("You may need to run this as administrator or check git installation.")
                        if input("Continue anyway? [y/N]: ").strip().lower() in ("y", "yes"):
                            return None
                        exit(1)
                elif choice == "2":
                    print("⚠️  Skipping this git command. Some features may not work properly.")
                    return None
                elif choice == "3":
                    print("❌ Aborting script.")
                    exit(1)
                else:
                    print("Please enter 1, 2, or 3.")
        
        print(f"\n❌ Error running: {' '.join(cmd)}")
        print(f"Exit code: {e.returncode}")
        print("\n💡 Common solutions:")
        if cmd[0] == "git":
            print("  • Check if git is properly installed and configured")
            print("  • Ensure you have proper permissions for this directory")
            print("  • Try running the command manually to see more details")
        print(f"\n🔧 Manual command to try: {' '.join(cmd)}")
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
        # If CLI arg provided, use it.
        if arg:
            path = os.path.abspath(os.path.expanduser(arg))
        else:
            # Try to open a GUI folder picker first (tkinter). If that fails or user
            # cancels, fall back to text input in the console.
            try:
                import tkinter as tk
                from tkinter import filedialog

                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                picked = filedialog.askdirectory(title='Select target folder for new repo')
                root.destroy()
                if picked:
                    path = os.path.abspath(picked)
                else:
                    # user cancelled GUI picker; fall back to console input
                    raise RuntimeError('GUI folder selection cancelled')
            except Exception:
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
            print(f"Folder '{path}' already appears to be a git repository.")
            # Check if there's an existing remote
            try:
                result = subprocess.run(["git", "-C", path, "remote", "get-url", "origin"], 
                                      capture_output=True, text=True, check=True)
                existing_remote = result.stdout.strip()
                print(f"Existing remote 'origin': {existing_remote}")
                choice = input("What would you like to do?\n1. Keep existing remote and continue\n2. Replace with new remote\n3. Abort\nChoice [1/2/3]: ").strip()
                if choice == "1":
                    return path, existing_remote  # Return both path and existing URL
                elif choice == "2":
                    return path, "REPLACE:" + existing_remote  # Signal to replace the remote
                else:
                    print("Aborting.")
                    exit(1)
            except subprocess.CalledProcessError:
                # No remote exists, proceed normally - this is exactly what our script helps with!
                print("Git repository exists but no remote configured. Perfect! We'll set that up for you.")
                return path, None

        return path, None  # Return path and None for URL when no existing repo

    target_result = choose_target_folder(cli_folder)
    if isinstance(target_result, tuple):
        target, existing_url = target_result
    else:
        target, existing_url = target_result, None
    
    os.chdir(target)

    # Use existing URL if available, otherwise ask for new one
    if existing_url and not existing_url.startswith("REPLACE:"):
        url = existing_url
        print(f"Using existing remote: {url}")
    else:
        if existing_url and existing_url.startswith("REPLACE:"):
            old_url = existing_url[8:]  # Remove "REPLACE:" prefix
            print(f"Current remote: {old_url}")
            print("🔄 You chose to replace the remote.")
        url = cli_url or input("Enter remote repository URL (https or git@): ").strip()
        
    if not url:
        print("No URL provided. Exiting.")
        exit(1)

    # Extract the old URL for comparison if we're replacing
    old_remote_url = None
    if existing_url and existing_url.startswith("REPLACE:"):
        old_remote_url = existing_url[8:]  # Remove "REPLACE:" prefix

    folder = os.path.basename(os.path.abspath(os.getcwd()))
    readme = "README.md"
    content = f"# {folder}\n\nThis repository was initialized by create_github_repo.py.\n"
    create_readme(readme, content)

    # If .git already exists, skip git init
    if os.path.isdir(os.path.join(os.getcwd(), ".git")):
        print("Existing git repository detected. Skipping 'git init'.")
        
        # Determine if we need to update the remote
        needs_remote_update = False
        if old_remote_url:
            # We're replacing a remote
            needs_remote_update = True
        elif not existing_url or (existing_url and not existing_url.startswith("REPLACE:")):
            # No existing remote, or keeping existing remote
            if not existing_url:
                needs_remote_update = True
            elif existing_url != url:
                needs_remote_update = True
        
        if needs_remote_update:
            if old_remote_url and old_remote_url == url:
                # Same URL, no need to change
                print("✅ Remote URL is the same. No changes needed.")
            elif old_remote_url:
                # Different URL, replace the remote
                print(f"🔄 Replacing remote from {old_remote_url} to {url}")
                
                # Method 1: Try git remote set-url (most reliable)
                try:
                    set_url_result = subprocess.run(["git", "remote", "set-url", "origin", url], 
                                                   capture_output=True, text=True, check=True)
                    print("✅ Successfully updated remote URL")
                except subprocess.CalledProcessError:
                    # Method 2: Fallback to remove+add
                    print("🔄 Trying remove and add method...")
                    try:
                        remove_result = subprocess.run(["git", "remote", "remove", "origin"], 
                                                     capture_output=True, text=True, check=False)
                        if remove_result.returncode == 0:
                            print("✅ Successfully removed existing remote")
                        else:
                            print(f"⚠️  Could not remove existing remote: {remove_result.stderr}")
                    except Exception as e:
                        print(f"⚠️  Exception removing remote: {e}")
                    
                    # Now add the new remote
                    result = run_cmd(["git", "remote", "add", "origin", url])
                    if result is None:
                        print("⚠️  Remote setup was skipped. You may need to configure it manually.")
            else:
                # No existing remote, add new one
                result = run_cmd(["git", "remote", "add", "origin", url])
                if result is None:
                    print("⚠️  Remote setup was skipped. You may need to configure it manually.")
        else:
            # Same URL, no need to change remote
            print("✅ Remote 'origin' already configured correctly.")
    else:
        result = run_cmd(["git", "init"])
        if result is None:
            print("⚠️  Git init was skipped. Manual git setup may be required.")
            return
        
        result = run_cmd(["git", "remote", "add", "origin", url])
        if result is None:
            print("⚠️  Remote setup was skipped. You may need to configure it manually.")

    # Continue with git operations, but check if each succeeds
    # First, let's see what changes exist
    try:
        status_result = subprocess.run(["git", "status", "--porcelain"], 
                                     capture_output=True, text=True, check=True)
        has_changes = bool(status_result.stdout.strip())
        
        if has_changes:
            print("📋 Detected changes in repository:")
            print(status_result.stdout)
            
            # Add all changes, not just README
            print("📦 Adding all changes...")
            result = run_cmd(["git", "add", "."])
            if result is None:
                print("⚠️  Could not add changes to git. You may need to do this manually.")
                return
            
            # Commit with a more appropriate message
            commit_msg = "Update repository with local changes"
            result = run_cmd(["git", "commit", "-m", commit_msg])
            if result is None:
                print("⚠️  Could not create commit. You may need to do this manually.")
                return
        else:
            # No changes detected, just add README if it's new
            result = run_cmd(["git", "add", readme])
            if result is None:
                print("⚠️  Could not add README to git. You may need to do this manually.")
                return
            
            result = run_cmd(["git", "commit", "-m", "first commit"])
            if result is None:
                # This is fine if there's nothing to commit
                print("ℹ️  No new changes to commit.")
    except subprocess.CalledProcessError:
        print("⚠️  Could not check git status. Trying to add README anyway...")
        result = run_cmd(["git", "add", readme])
        if result is None:
            print("⚠️  Could not add README to git.")
            return
    
    result = run_cmd(["git", "branch", "-M", "main"])
    if result is None:
        print("⚠️  Could not rename branch to main. You may be on an older git version.")
    
    # Try to push, handle different scenarios
    print("🚀 Pushing to remote repository...")
    result = run_cmd(["git", "push", "-u", "origin", "main"])
    if result is None:
        print("⚠️  Initial push failed. This might be due to existing content in the remote.")
        print("🔄 Trying force push (this will overwrite remote content)...")
        
        choice = input("Do you want to force push? This will overwrite any existing content in the remote repo [y/N]: ").strip().lower()
        if choice in ("y", "yes"):
            result = run_cmd(["git", "push", "-f", "-u", "origin", "main"])
            if result is None:
                print("⚠️  Force push also failed. You may need to check:")
                print("  • Repository permissions")
                print("  • Network connection")
                print("  • Authentication (SSH keys or personal access token)")
                print(f"\n🔧 Manual commands to try:")
                print(f"  git push -u origin main")
                print(f"  git push -f -u origin main  # (force push)")
                return
            else:
                print("✅ Force push successful!")
        else:
            print("⚠️  Push cancelled. You may need to:")
            print("  • Pull remote changes first: git pull origin main")
            print("  • Or force push: git push -f -u origin main")
            print(f"\n🔧 Manual commands to try:")
            print(f"  git pull origin main --allow-unrelated-histories")
            print(f"  git push -u origin main")
            return
    else:
        print("✅ Push successful!")
    
    print("✅ Done! Repository has been successfully created and pushed to remote.")


if __name__ == "__main__":
    main()
