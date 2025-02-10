import os
import json
import requests
import datetime
import time

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

# Load GitHub Token from Environment Variable
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GitHub token is required. Set it using 'export GITHUB_TOKEN=your_token'.")

# Set headers for API requests
HEADERS = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Time Window for Stale Branches (1 Year)
TIME_WINDOW = datetime.datetime.utcnow() - datetime.timedelta(days=365)

# File to Store Execution Progress
#PROGRESS_FILE = "repoCleaner_progress.json"


def load_repositories(file_path="masterRepoList.txt"):
    """Reads repository list from a file."""
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Ensure the file exists with repo list.")
        return []


def get_branches(repo):
    """Fetches all branches in a repository."""
    url = f"{GITHUB_API_URL}/repos/{repo}/branches"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Error: Unauthorized. Check your GitHub token permissions.")
        exit(1)
    elif response.status_code == 404:
        print(f"Error: Repository {repo} not found.")
        return []
    else:
        print(f"Failed to fetch branches for {repo}: {response.status_code}")
        return []


def get_last_commit_date(repo, branch):
    """Gets the latest commit date for a given branch."""
    url = f"{GITHUB_API_URL}/repos/{repo}/commits/{branch}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        commit_date = response.json()["commit"]["committer"]["date"]
        return datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
    return None


def identify_stale_branches(repo):
    """Identifies stale branches in a repository."""
    stale_branches = []
    all_branches = get_branches(repo)

    for branch in all_branches:
        branch_name = branch["name"]
        commit_date = get_last_commit_date(repo, branch_name)

        if commit_date and commit_date < TIME_WINDOW:
            stale_branches.append((branch_name, commit_date))

    return all_branches, stale_branches


def user_confirmation(stale_branches):
    """Prompts user to select stale branches for deletion."""
    print("\nStale Branches Detected:")

    for i, (branch, date) in enumerate(stale_branches):
        print(f"[{i}] {branch} (Last commit: {date.strftime('%Y-%m-%d')})")

    selection = input("Enter the numbers of branches to delete (comma-separated, or 'all' to delete all): ")

    if selection.lower() == "all":
        return [branch for branch, _ in stale_branches]

    try:
        indices = [int(i) for i in selection.split(",") if i.isdigit() and int(i) < len(stale_branches)]
        return [stale_branches[i][0] for i in indices]
    except Exception:
        print("Invalid selection. No branches deleted.")
        return []


def delete_branches(repo, branches):
    """Deletes selected branches from the repository."""
    for branch in branches:
        url = f"{GITHUB_API_URL}/repos/{repo}/git/refs/heads/{branch}"
        response = requests.delete(url, headers=HEADERS)

        if response.status_code == 204:
            print(f" Deleted branch: {branch}")
        else:
            print(f" Failed to delete {branch}: {response.status_code}")


def generate_summary(repo, total_branches, stale_branches, deleted_branches):
    """Generates an executive summary."""
    summary = {
        "repository": repo,
        "total_branches": len(total_branches),
        "stale_branches": len(stale_branches),
        "deleted_branches": deleted_branches,
        "recommend_repo_deletion": len(stale_branches) == len(total_branches)
    }

    with open("cleanup_summary.json", "a") as f:
        json.dump(summary, f, indent=4)
        f.write("\n")

    print(f" Summary saved for {repo} in cleanup_summary.json")


def save_progress(repo, stale_branches, deleted_branches):
    """Saves execution progress in case of failure."""
    # Convert datetime objects to string format before saving
    progress = {
        "repo": repo,
        "stale_branches": [{ "branch": branch, "last_commit": date.strftime('%Y-%m-%d') } for branch, date in stale_branches],
        "deleted_branches": deleted_branches
    }

    with open("repoCleaner_progress.json", "a") as f:
        json.dump(progress, f, indent=4)
        f.write("\n")

    print(f" Progress saved for {repo} in repoCleaner_progress.json")


def main():
    """Main function to execute repo cleaning."""
    repositories = load_repositories()

    if not repositories:
        print("No repositories found. Exiting.")
        return

    for repo in repositories:
        print(f"\n Processing: {repo}")

        total_branches, stale_branches = identify_stale_branches(repo)
        print(f" Total branches in {repo}: {len(total_branches)}")
        print(f" Stale branches (>1 year old): {len(stale_branches)}")

        if not stale_branches:
            print(f"No stale branches found in {repo}. Skipping...\n")
            continue

        deleted_branches = user_confirmation(stale_branches)

        if deleted_branches:
            delete_branches(repo, deleted_branches)

        generate_summary(repo, total_branches, stale_branches, deleted_branches)
        save_progress(repo, stale_branches, deleted_branches)


if __name__ == "__main__":
    main()
