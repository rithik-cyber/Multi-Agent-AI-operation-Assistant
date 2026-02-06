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
def run_task(request: UserRequest):

    logger.info(f"Received Task: {request.task}")

    #  Planner Execution + Timing
    plan, planner_time = create_plan(request.task)

    #  Executor Execution + Timing
    execution_result, executor_time = execute_plan(plan)

    #  Verifier Execution + Timing
    verified_output, verifier_time = verify_results(execution_result)

    # Total Time
    total_time = round(planner_time + executor_time + verifier_time, 3)

    return {
        "task": request.task,
        "plan": plan,
        "result": verified_output,
        "timing": {
            "planner_time": planner_time,
            "executor_time": executor_time,
            "verifier_time": verifier_time,
            "total_time": total_time
        }
    }




