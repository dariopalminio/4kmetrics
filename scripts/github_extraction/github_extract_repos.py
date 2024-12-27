import requests
from github_extraction.github_pagination_helper import extract_max_pages
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
    pages_max = 1
    list = []
    while page <= pages_max:
        api_url = f'{repositories_url}?page={page}'
        try:
            response = github_client_get(api_url)
            if page == 1: 
                pages_max = extract_max_pages(response.headers.get('Link'))
            data = response.json()
            list.extend([{"name": item["name"]} for item in data])
            page += 1
        except Exception as e:
            print(f"Failed to get a valid response from: {api_url}, due to {e}")
            break
    return list


