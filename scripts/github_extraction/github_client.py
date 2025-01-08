import os
import time
import requests

def github_client_get(url, params=None):
    """
    Performs a GET request to the specified URL using Bearer authentication with the GitHub token.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GitHub token GITHUB_TOKEN not found in environment variables.")
    
    headers_config = {
        "Authorization": f'Bearer {github_token}',
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    for attempt in range(3):
        response = requests.get(url, headers=headers_config, params=params)
        remaining = response.headers.get('X-RateLimit-Remaining')
        limit = response.headers.get('X-RateLimit-Limit')
        used = response.headers.get('X-RateLimit-Used')
        print(f"API call --> Request to {url}, Of the total limit of {limit} requests, {used} has been used, and there are {remaining} remaining.")
        if response.ok:
            return response
        elif response.status_code in {403, 429}:
            print("Rate limit error handling, response.status_code:", response.status_code)
            wait_until_rate_limit_resets(response)
        else:
            response.raise_for_status()
    raise RuntimeError("Failed to complete request after 3 attempts.")

def wait_until_rate_limit_resets(response):
    """Wait until the GitHub rate limit resets."""
    MAX_WAIT_TIME = 7200  # 2 hs in sec
    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time()))
    wait_seconds = max(reset_time - time.time(), 1)
    if wait_seconds > MAX_WAIT_TIME:
        error_msg = f"Rate limit reset time ({wait_seconds} seconds) exceeds maximum wait time of {MAX_WAIT_TIME} seconds."
        print(f"Exiting due to: {error_msg}")
        raise RuntimeError(error_msg)
    print(f"Rate limit exceeded. Waiting for {wait_seconds} seconds...")
    time.sleep(wait_seconds)


