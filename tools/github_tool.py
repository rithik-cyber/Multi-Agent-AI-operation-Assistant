import os
import requests
from dotenv import load_dotenv
from llm.logger import logger

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def search_github_repositories(query, limit=5):
    logger.info(f"Searching GitHub repos for: {query}")

    url = "https://api.github.com/search/repositories"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        results = []
        for repo in data.get("items", []):
            results.append({
                "name": repo["name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "description": repo["description"]
            })

        return results

    except Exception as e:
        logger.error(f"GitHub API error: {e}")
        return {"error": str(e)}
