#!/usr/bin/env python
# encoding: utf-8
import json
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
    while True:
        api_url = f'https://api.github.com/orgs/{GITHUB_ORG}/teams?page={page}'
        response = github_client_get(api_url)
        data = response.json()
        teams.extend([
            {
            "id": item["id"],
            "name": item["name"], 
            "repositories_url": item["repositories_url"], 
            "repositories_list": []
            } for item in data])
        if 'next' in response.links:
            page += 1
        else:
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
    while True:
        api_url = f'https://api.github.com/orgs/{GITHUB_ORG}/teams?page={page}'
        response = github_client_get(api_url)
        data = response.json()
        for item in data:
            if (item["name"].lower() == team_name.lower()):
                team_info = {
                    "id": item["id"],
                    "name": item["name"], 
                    "repositories_url": item["repositories_url"], 
                    "repositories_list": []
                    } 
                return team_info
        if 'next' in response.links:
            page += 1
        else:
            break
    return team_info

