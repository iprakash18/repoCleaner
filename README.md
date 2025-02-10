# repoCleaner

# Prerequisites

	Python 3.x installed
	A GitHub Personal Access Token (PAT) with the required permissions.

# Installation:

Clone the repository
	
 	git clone https://github.com/your-username/repoCleaner.git
	cd repoCleaner

# GitHub Token Setup:

Generate a Personal Access Token (PAT) from GitHub with the following scopes:

	repo (Full control of private repositories)
	delete:repo (Required to delete branches)

Export the token as an environment variable:
	
	export GITHUB_TOKEN=your_token_here	# For Linux
	set GITHUB_TOKEN=your_token # For Windows

	

# Usage:

Create a file masterRepoList.txt and list all repositories (one per line) in the format:
	
	username/repository-name
	organization/repository-name

Run the script:
	
	python repoCleaner.py

3. Follow the interactive prompts to delete stale branches.

# Output:

	cleanup_summary.json: Stores a summary of deleted branches per repository.
	repoCleaner_progress.json: Logs execution progress to resume later if interrupted.

Example:

	C:\Users\GL277UX\OneDrive\Desktop\repoCleaner>py repoCleaner.py
	
	📌 Processing: github/docs
	🔍 Total branches in github/docs: 30
	🕒 Stale branches (>1 year old): 19
	
	Stale Branches Detected:
	[0] cmwilson21-patch-1 (Last commit: 2023-07-06)
	[1] dependabot/docker/node-19.1.0-alpine (Last commit: 2022-11-17)
	[2] dependabot/docker/node-19.7-alpine (Last commit: 2023-02-23)
	[3] dependabot/docker/node-19.9-alpine (Last commit: 2023-04-13)
	[4] dependabot/docker/node-20.4-alpine (Last commit: 2023-07-13)
	[5] dependabot/docker/node-20.5-alpine (Last commit: 2023-07-26)
	[6] dependabot/docker/node-20.8-alpine (Last commit: 2023-10-19)
	[7] dependabot/github_actions/actions/cache-4.0.0 (Last commit: 2024-01-17)
	[8] dependabot/github_actions/actions/github-script-98814c53be79b1d30f795b907e553d8679345975 (Last commit: 2023-02-01)
	[9] dependabot/github_actions/juliangruber/approve-pull-request-action-2 (Last commit: 2022-10-21)
	[10] dependabot/npm_and_yarn/change-case-5.0.1 (Last commit: 2023-10-03)
	[11] dependabot/npm_and_yarn/follow-redirects-1.15.4 (Last commit: 2024-01-09)
	[12] dependabot/npm_and_yarn/jest-environment-puppeteer-8.0.5 (Last commit: 2023-03-14)
	[13] dependabot/npm_and_yarn/jest-environment-puppeteer-8.0.6 (Last commit: 2023-03-28)
	[14] dependabot/npm_and_yarn/lint-staged-15.0.1 (Last commit: 2023-10-17)
	[15] dependabot/npm_and_yarn/liquidjs-10.4.0 (Last commit: 2023-01-03)
	[16] dependabot/npm_and_yarn/liquidjs-10.6.0 (Last commit: 2023-02-28)
	[17] dependabot/npm_and_yarn/liquidjs-10.6.1 (Last commit: 2023-03-07)
	[18] dependabot/npm_and_yarn/liquidjs-10.6.2 (Last commit: 2023-03-21)
	Enter the numbers of branches to delete (comma-separated, or 'all' to delete all): 1
	❌ Failed to delete dependabot/docker/node-19.1.0-alpine: 403
	📄 Summary saved for github/docs in cleanup_summary.json
	🔄 Progress saved for github/docs in repoCleaner_progress.json

