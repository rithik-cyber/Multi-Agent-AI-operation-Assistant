import requests
from utils.retry_timer import retry


@retry(max_attempts=3, delay=2)
def search_github_repositories(query):

    url = f"https://api.github.com/search/repositories?q={query}&sort=stars"

    response = requests.get(url, timeout=5)

    data = response.json()

    results = []

    for repo in data["items"][:5]:
        results.append({
            "name": repo["name"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "description": repo["description"]
        })

    return results
