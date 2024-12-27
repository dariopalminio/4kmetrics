#!/usr/bin/env python
# encoding: utf-8
import json
import requests
from github_extraction.github_pagination_helper import extract_max_pages
from github_extraction.github_client import github_client_get

def get_teams(GITHUB_ORG):
    """
    Retrieve a list of all teams within a specified GitHub organization visible to the authenticated user.
    
    This function utilizes GitHub's REST API to fetch teams, handling pagination automatically.
    The response is paginated and each page is processed sequentially until all pages have been retrieved.
    
    Usage of GitHub API:
    - Documentation: https://api.github.com/orgs/ORG/teams
    """
    teams = []
    page = 1
    pages_max = 1
    while page <= pages_max:
        api_url = f'https://api.github.com/orgs/{GITHUB_ORG}/teams?page={page}'
        try:
            response = github_client_get(api_url)
            if page == 1: 
                pages_max = extract_max_pages(response.headers.get('Link'))
            data = response.json()
            teams.extend([
                {
                "id": item["id"],
                "name": item["name"], 
                "repositories_url": item["repositories_url"], 
                "repositories_list": []
                } for item in data])
            page += 1
        except Exception as e:
            print(f"Failed to get a valid response from: {api_url}, due to {e}")
            break
    return teams

def get_team_info(GITHUB_ORG, team_name):
    """
    Retrieve a list of all teams within a specified GitHub organization visible to the authenticated user.
    
    This function utilizes GitHub's REST API to fetch teams, handling pagination automatically.
    The response is paginated and each page is processed sequentially until all pages have been retrieved.
    
    Usage of GitHub API:
    - Documentation: https://api.github.com/orgs/ORG/teams
    """
    team_info = {}

    page = 1
    pages_max = 1
    while page <= pages_max:
        api_url = f'https://api.github.com/orgs/{GITHUB_ORG}/teams?page={page}'
        try:
            response = github_client_get(api_url)
            if page == 1: 
                pages_max = extract_max_pages(response.headers.get('Link'))
            data = response.json()
            for item in data:
                if (item["name"] == team_name):
                    team_info = {
                        "id": item["id"],
                        "name": item["name"], 
                        "repositories_url": item["repositories_url"], 
                        "repositories_list": []
                        } 
                    return team_info
            page += 1
        except Exception as e:
            print(f"Failed to get a valid response from: {api_url}, due to {e}")
            break
    return team_info