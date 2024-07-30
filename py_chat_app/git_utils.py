import subprocess
import os
import shutil

def clone_github_repo(repo_url, clone_dir):
    if not repo_url.startswith("https://github.com/") and not repo_url.startswith("git@github.com:"):
        print("Invalid GitHub repository URL.")
        return None
    
    # Clean up existing clone_dir if it exists
    if os.path.exists(clone_dir):
        try:
            shutil.rmtree(clone_dir)
            print(f"Removed existing directory: {clone_dir}")
        except Exception as e:
            print(f"Error removing existing directory {clone_dir}: {e}")
            return None
    
    try:
        clone_command = ["git", "clone", repo_url, clone_dir]
        subprocess.run(clone_command, check=True)
        print(f"Repository cloned successfully from {repo_url}")
        return clone_dir
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while cloning the repository: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None
