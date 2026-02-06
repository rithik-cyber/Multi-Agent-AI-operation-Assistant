from llm.logger import logger


def verify_results(execution_result):
    logger.info("Verifier agent started")

    verified_output = {
        "status": "success",
        "data": execution_result,
        "issues": []
    }

    try:
        for key, value in execution_result.items():

            if isinstance(value, dict) and "error" in value:
                verified_output["status"] = "partial_success"
                verified_output["issues"].append(
                    f"{key} tool returned error: {value['error']}"
                )

        return verified_output

    except Exception as e:
        logger.error(f"Verifier error: {e}")
        return {
            "status": "failure",
            "error": str(e)
        }
