from llm.logger import logger
from tools.github_tool import search_github_repositories
from tools.weather_tool import get_weather


def execute_plan(plan):
    logger.info("Executor agent started")

    results = {}

    try:
        steps = plan.get("steps", [])

        for step in steps:
            tool = step.get("tool")
            user_input = step.get("input")

            logger.info(f"Executing tool: {tool} with input: {user_input}")

            
            # GitHub Tool 
            
            if tool == "github_search":

                if "github" not in results:
                    results["github"] = []

                repos = search_github_repositories(user_input)
                results["github"].extend(repos)

            
            # Weather Tool 
            
            elif tool == "weather":

                if "weather" not in results:
                    results["weather"] = []

                weather_data = get_weather(user_input)
                results["weather"].append(weather_data)

            else:
                results[tool] = {"error": "Unknown tool"}

        return results

    except Exception as e:
        logger.error(f"Executor error: {e}")
        return {"error": str(e)}

