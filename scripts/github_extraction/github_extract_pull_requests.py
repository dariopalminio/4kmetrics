#!/usr/bin/env python
# encoding: utf-8
import json
import requests
from github_extraction.github_pagination_helper import extract_max_pages
from github_extraction.github_client import github_client_get
from datetime import datetime

def extract_pr_list_from_repo_between_dates(GITHUB_ORG, repo_name, start_date, end_date):
    """
    Finds and loads all indicated pull request from the indicated repository name, between two dates, with status successful. 
    /repos/{owner}/{repo}/pulls
    with Query parameters state = closed
    curl -L 
    -H "Accept: application/vnd.github+json" 
    -H "Authorization: Bearer <YOUR-TOKEN>" 
    -H "X-GitHub-Api-Version: 2022-11-28" 
    https://api.github.com/repos/OWNER/REPO/pulls
    """
    query_params = {
        "state": "closed",
        "since": start_date,
        "until": end_date
    }

    OWNER = GITHUB_ORG
    pull_requests = []
    page = 1
    pages_max = 1
    while page <= pages_max:
        api_url = f'https://api.github.com/repos/{OWNER}/{repo_name}/pulls?page={page}'
        try:
            response = github_client_get(api_url, params=query_params)
            if page == 1: 
                pages_max = extract_max_pages(response.headers.get('Link'))
            data = response.json()
            for item in data:
                element = process_pull_request(GITHUB_ORG, item)
                if element:
                    pull_requests.append(element)
            page += 1
        except Exception as e:
            print(f"Failed to get a valid response from: {api_url}, due to {e}")
            break
    
    for pr in pull_requests:
        extract_cycle_time(GITHUB_ORG, pr)

    return pull_requests

def process_pull_request(GITHUB_ORG, pr_json):
    """
    Process a single GitHub json item to extract details about pull request in the production branch.
    This function filters and processes 'Pull request' types from a GitHub JSON object. It extracts
    and returns relevant details only if the event is merged to the 'production' (main or master) branch.
    """
    metadata = json.dumps(pr_json)  #JSON string containing the complete event data

    if is_merged_to_production(pr_json):
    
        github_pr = {
                "id": pr_json["id"],
                "title": pr_json["title"],
                "number": pr_json["number"],
                "state": pr_json["state"],
                "created_at": pr_json["created_at"],
                "first_commited_at": None,
                "merged_at": pr_json["merged_at"],
                "labels": process_labels_to_str(pr_json["labels"]),
                "repo_name": last_part(pr_json["base"].get("repo").get("name")),
                "branch_origin": pr_json["head"].get("ref"),
                "branch_end": pr_json["base"].get("ref"),
                "commits_url": pr_json["commits_url"],
                "is_fix": False,
                "is_hotfix": False,
                "is_rollback": False,
                "is_feature": False,
                "cycle_time_in_days": None
        }

        github_pr["is_fix"] = is_fix(github_pr)
        github_pr["is_hotfix"] = is_hotfix(github_pr)
        github_pr["is_rollback"] = is_rollback(github_pr)
        github_pr["is_feature"] = is_feature(github_pr)

        return github_pr

    else:
        return None

def is_merged_to_production(pr_json):
    production_branch = {"refs/heads/master", "refs/heads/main", "refs/heads/production", "master", "main", "production"}
    return ((pr_json["base"].get("ref") in production_branch) and pr_json["merged_at"] is not None)

def process_labels_to_str(labels_json):
    labels = []
    for item in labels_json:
        labels.append(item["name"])
    return ",".join(labels)

def is_feature(github_pr):
    text_lower = f"{github_pr["title"].lower()},{github_pr["labels"].lower()},{github_pr["branch_origin"].lower()}"
    #contains feat?
    if ('feat' in text_lower or 'enhancement' in text_lower):
        return True
    #contains refactor?
    if ('refactor' in text_lower):
        return True
    #contains test?
    if ('test' in text_lower):
        return True
    #contains style?
    if ('style' in text_lower):
        return True
    #contains performance or chore?
    if ('perf' in text_lower):
        return False
    return False

def is_fix(github_pr):
    text_lower = f"{github_pr["title"].lower()},{github_pr["labels"].lower()},{github_pr["branch_origin"].lower()}"
    #contains bug fix?
    if (('type: fix' in text_lower or 'bug' in text_lower or 'bugfix' in text_lower or 'bug-fix' in text_lower or 'bug fix' in text_lower)):
        return True
    #contains hotfix?
    if ('hotfix' in text_lower or 'hot-fix' in text_lower or 'hot fix' in text_lower):
        return True
    return False

def is_hotfix(github_pr):
    text_lower = f"{github_pr["title"].lower()},{github_pr["labels"].lower()},{github_pr["branch_origin"].lower()}"
    #title contains hotfix?
    if ('hotfix' in text_lower or 'hot-fix' in text_lower or 'hot fix' in text_lower or 'type:hotfix' in text_lower):
        return True
    return False

def is_rollback(github_pr):
    text_lower = f"{github_pr["title"].lower()},{github_pr["labels"].lower()},{github_pr["branch_origin"].lower()}"
    #contains rollback or revert?
    if ('rollback' in text_lower or 'roll-back' in text_lower or 'revert' in text_lower):
        return True
    return False

def last_part(path):
    if not path:
        return ''  
    parts = path.split('/')
    return parts[-1]

def extract_cycle_time(GITHUB_ORG, pr):
    first_commit_date = extract_first_commit_date(GITHUB_ORG, pr['commits_url'])
    if first_commit_date is not None:
        pr['first_commited_at'] = first_commit_date
        if pr['merged_at'] is not None:
            #Cycle time is calculated using the date of the first commit and the date of the merged
            pr['cycle_time_in_days'] = calculate_cycle_time(pr['first_commited_at'], pr['merged_at'])
    return pr

def extract_first_commit_date(GITHUB_ORG, commits_url):
    OWNER = GITHUB_ORG
    first_commit_date = None
    page = 1
    pages_max = 1
    while page <= pages_max:
        try:
            response = github_client_get(commits_url)
            if page == 1: 
                pages_max = extract_max_pages(response.headers.get('Link'))
            data = response.json()
            for item in data:
                commit_date = item['commit']['author']['date'] #The author date indicates when the original change was made.
                if first_commit_date is None:
                    first_commit_date = commit_date
                else: 
                    date1 = datetime.fromisoformat(first_commit_date.replace('Z', ''))
                    date2 = datetime.fromisoformat(commit_date.replace('Z', ''))
                    if date2 < date1:
                        first_commit_date = commit_date
            page += 1
        except Exception as e:
            print(f"Failed to get a valid response from: {commits_url}, due to {e}")
            break
    return first_commit_date

def calculate_cycle_time(date_str_1: str, date_str_2: str) -> float:
    """
    Calculates the difference in days between two given dates in ISO 8601 format.

    :param fecha_str_1: Start date in format 'YYYY-MM-DDTHH:MM:SSZ'.
    :param fecha_str_2: End date in format 'YYYY-MM-DDTHH:MM:SSZ'.
    :return: Difference in days as an integer.
    """
    # Parse strings into datetime objects:
    date_dt_1 = datetime.strptime(date_str_1, "%Y-%m-%dT%H:%M:%SZ")
    date_dt_2 = datetime.strptime(date_str_2, "%Y-%m-%dT%H:%M:%SZ")

    # Calculate the difference in days:
    difference = date_dt_2 - date_dt_1

    # Convert seconds to days
    difference_in_days = difference.total_seconds() / (60 * 60 * 24) 

    # Round to four decimal places:
    difference_in_days = round(difference_in_days, 4)
    return difference_in_days
