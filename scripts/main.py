import os
from dotenv import load_dotenv
from utils.title_decorator import print_decorated_title
from github_extraction.github_extract_pull_requests import extract_pr_list_from_repo_between_dates
from github_extraction.github_extract_teams import get_team_info
from github_extraction.github_extract_repos import get_repos_name_list   

# Load Environment Variables
try:
    load_dotenv()

    # Github Organization & Token
    GITHUB_ORG = os.getenv("GITHUB_ORG")
    if not GITHUB_ORG:
        raise ValueError("GITHUB_ORG not found in environment variables.")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        raise ValueError("GitHub token GITHUB_TOKEN not found in environment variables.")

    # Welcome message
    print_decorated_title('Welcome to 4 Key Metrics project: The goal of this Script is to extract historical data from GitHub') 
    print("With a indicated team name, it will search its repositories and all closed Pull requests between two indicated dates, from github org (GITHUB_ORG): ")
    print(f'{GITHUB_ORG}')
except Exception as e:
    print("An error occurred while loading environment variables:", e)
    raise e

# Extract all closed Pull requests from a team
try:
    # Extract team info with repositories list
    team_name = input("Enter a github team name: ") 
    team_info = {}
    team_info = get_team_info(GITHUB_ORG, team_name)
    team_repos_list = get_repos_name_list(team_info["repositories_url"])
    print(f"REPOS:{team_repos_list}")
    team_info["repositories_list"] = team_repos_list

    # Extracting list of closed pull requests
    print('Extract list of closed PRs from the indicated repositories, between two dates.')
    start_date = input("Enter a start date with format YYYY-MM-DD: ")
    end_date = input("Enter a end date  with format YYYY-MM-DD: ")
    start_date = start_date + "T00:00:00Z"
    end_date = end_date + "T00:00:00Z"
    pull_requests = []
    for repo in team_info["repositories_list"]:
        pr_list = extract_pr_list_from_repo_between_dates(GITHUB_ORG, repo["name"], start_date, end_date)
        pull_requests.extend(pr_list)
    print(pull_requests)
except Exception as e:
    print("An error occurred while fetching data from github:", e)
    raise e
