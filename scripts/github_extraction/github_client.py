import os
import time
import requests

def github_client_get(url, params=None):
    """
    Performs a GET request to the specified URL using Bearer authentication with the GitHub token.

    This function attempts to handle rate limits imposed by the GitHub API. If it encounters a rate limit error (HTTP 403 Forbidden or 429 Too Many Requests), or if the 'X-RateLimit-Remaining' header indicates no more requests are allowed, it waits until the limit is reset as indicated by the 'X-RateLimit-Reset' header before retrying the request.

    Args:
        url (str): The URL to make the GET request to.

    Returns:
        requests.Response: The response object from the request if it was successful.
        None: If the request could not be completed after the maximum number of retries or if the GitHub token was not found.

    Raises:
        ValueError: If the GitHub token is not found in environment variables.
        RuntimeError: If the maximum number of retries is exceeded due to continuous request errors.

    The function uses environment variables to obtain the GitHub authentication token ('GITHUB_TOKEN') and defines a maximum of three retries for requests that fail specifically due to rate limits. For other types of HTTP request errors, the exception is raised immediately.
    """
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        raise ValueError("GitHub token GITHUB_TOKEN not found in environment variables.")
    
    headers_auth = {
        "Authorization": f'Bearer {GITHUB_TOKEN}',
        "Accept": "application/vnd.github+json"
        # ,"X-GitHub-Api-Version": "2022-11-28"
    }
    
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers_auth, params=params)
            remaining = response.headers.get('X-RateLimit-Remaining')
            limit = response.headers.get('X-RateLimit-Limit')
            used = response.headers.get('X-RateLimit-Used')
            print(f"API call --> Request to {url}, Of the total limit of {limit} requests, {used} has been used, and there are {remaining} remaining.")
            
            if response.status_code in [403, 429] or remaining == '0':
                # Rate limit error handling
                print("Rate limit error handling, response.status_code:", response.status_code)
                if response.status_code == 403:
                    print("403 Forbidden or token error")
                wait_seconds = 60  # Default wait time
                reset_time = response.headers.get('X-RateLimit-Reset')
                
                if remaining == '0' and reset_time:
                    # Calculate wait time until rate limit reset
                    current_time = time.time()
                    reset_time = int(reset_time)
                    wait_time = reset_time - current_time
                    print(f"Rate limit reached. The value of X-RateLimit-Reset is {reset_time}; ")
                    print(f"Rate limit reached. Waiting for {wait_time} time before retrying... ")
                    wait_seconds = max(wait_time, 1)
                
                print(f"Waiting for {wait_seconds} seconds before retrying...")
                time.sleep(wait_seconds)
                retry_count += 1
                continue
            
            if response.ok:
                return response
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            retry_count += 1
            if retry_count == max_retries:
                raise RuntimeError("Max retries exceeded.") from e # throw exception up

    
