import os
from dotenv import load_dotenv
from utils.title_decorator import print_decorated_title
from github_extraction.github_extract_pull_requests import extract_pr_list_from_repo_between_dates
from github_extraction.github_extract_teams import get_team_info
from github_extraction.github_extract_repos import get_repos_name_list

print_decorated_title('Welcome to 4 Key Metrics project: The goal of this Script is to extract historical data from GitHub')    

# Environment Variables
load_dotenv()


GITHUB_ORG = os.getenv("GITHUB_ORG")
if not GITHUB_ORG:
    raise ValueError("GITHUB_ORG not found in environment variables.")
print(f'Your github org is (GITHUB_ORG): {GITHUB_ORG}')

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token GITHUB_TOKEN not found in environment variables.")

input("Press a key to continue: ")

# Extract team info with repositories list
print('My team...')
team_name = "BrigadaA"
team_info = {}
team_info = get_team_info(GITHUB_ORG, team_name)
team_repos_list = get_repos_name_list(team_info["repositories_url"])
print("REPOS:")
print(team_repos_list)
team_info["repositories_list"] = team_repos_list
print("team_repos_list:")
print(team_info)

# Extract Pull Request of team indicated
print('Extracting pull request list...')
start_date = "2024-01-01T00:00:00Z"
end_date = "2024-04-30T23:59:59Z"

pull_requests = []
for repo in team_info["repositories_list"]:
    pr_list = extract_pr_list_from_repo_between_dates(GITHUB_ORG, repo["name"], start_date, end_date)
    pull_requests.extend(pr_list)
print(pull_requests)
