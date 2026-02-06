import json
import re
from llm.llm_config import client
from llm.logger import logger


def extract_json(text):
    """Extract JSON block from LLM response."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def create_plan(user_task):
    logger.info("Planner agent started")

    prompt = f"""
You are a planning AI agent.

Your job is to convert the user task into a structured JSON plan.

Available tools:
1. github_search → Use for searching GitHub repositories
2. weather → Use for getting weather of a city

Return ONLY valid JSON in this format:
{{
  "steps": [
    {{"tool": "tool_name", "input": "user_input"}}
  ]
}}

User Task:
{user_task}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content
        logger.info(f"Planner raw output: {content}")

        json_text = extract_json(content)

        if not json_text:
            raise ValueError("No JSON found in planner output")

        plan = json.loads(json_text)

        return plan

    except Exception as e:
        logger.error(f"Planner error: {e}")
        return {"error": str(e)}
