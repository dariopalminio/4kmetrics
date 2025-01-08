import requests
from github_extraction.github_client import github_client_get


def get_teams_with_their_repository_lists(teams_data):
    """
    From a list of teams, it retrieves its list of repositories for each team and includes them in the returned data structure.
    """
    try:
        for team in teams_data:
            repositories_url = team.get("repositories_url")
            team.get("repositories_list").extend(get_repos_name_list(repositories_url))
        return teams_data
    except requests.exceptions.RequestException as e:
        print(f"Error getting repositories from GitHub: {e}")
        return None

def get_repos_name_list(repositories_url):
    """
    Retrieves the list of repositories names indicated in the argument url.
    
    This function utilizes GitHub's REST API to fetch repositories, handling pagination automatically.
    The response is paginated and each page is processed sequentially until all pages have been retrieved.
    
    Usage of GitHub API:
    - repositories_url example: https://api.github.com/organizations/87711415/team/3442512/repos
    """
    page = 1
    list = []
    while True:
        api_url = f'{repositories_url}?page={page}'
        response = github_client_get(api_url)
        data = response.json()
        list.extend([{"name": item["name"]} for item in data])
        if 'next' in response.links:
            page += 1
        else:
            break
    return list


