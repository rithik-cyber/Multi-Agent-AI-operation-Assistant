from fastapi import FastAPI
from pydantic import BaseModel
from llm.logger import logger
from agents.planner import create_plan
from agents.executor import execute_plan
from agents.verifier import verify_results

app = FastAPI(title="AI Ops Assistant")

# Request Schema
class UserRequest(BaseModel):
    task: str

# Root Endpoint
@app.get("/")
def home():
    logger.info("Health check endpoint called")
    return {"message": "AI Ops Assistant Running"}

# Task Endpoint
@app.post("/run-task")
@app.post("/run-task")
def run_task(request: UserRequest):
    logger.info(f"Received Task: {request.task}")

    plan = create_plan(request.task)
    execution_result = execute_plan(plan)
    verified_output = verify_results(execution_result)

    return {
        "task": request.task,
        "plan": plan,
        "result": verified_output
    }



