import subprocess
import sys

def check_for_updates(repo_dir, remote='origin', branch='master'):
    """
    Checks for updates in the specified repository directory, and updates if the user agrees.
    :param repo_dir: Directory of the local Git repository.
    :param remote: Name of the remote repository (default is 'origin').
    :param branch: Name of the branch to check for updates (default is 'master').
    """
    # Navigate to the repository directory
    subprocess.run(['cd', repo_dir], shell=True)

    # Fetch the latest changes from the remote without merging
    subprocess.run(['git', 'fetch', remote], cwd=repo_dir)

    # Check if there are updates by comparing local and remote branches
    status = subprocess.run(['git', 'diff', f'{remote}/{branch}'], cwd=repo_dir, capture_output=True, text=True)

    if status.stdout:
        print("Updates are available.")
        user_decision = input("Do you want to update the repository? [y/n]: ")

        if user_decision.lower() in ['y', 'yes']:
            # Pull and merge the changes
            subprocess.run(['git', 'pull', remote, branch], cwd=repo_dir)
            print("Repository has been updated.")
        else:
            print("Update canceled by the user.")
    else:
        print("Your repository is up to date.")

# Example usage:
repo_dir = '/path/to/your/local/SJTU_tennis'  # Adjust this path to your local repository's location
check_for_updates(repo_dir)
