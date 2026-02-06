import streamlit as st
import requests

st.set_page_config(page_title="AI Operations Assistant", layout="wide")

st.title("AI Operations Assistant")
st.write("Multi-Agent AI System (Planner → Executor → Verifier)")

# Architecture Panel

with st.expander("System Architecture Overview"):
    st.markdown("""
Planner Agent  
- Converts user query into structured execution plan.

Executor Agent  
- Calls external APIs such as GitHub and Weather services.

Verifier Agent  
- Validates execution results.
""")


# Task Input

task = st.text_area(
    "Enter your task",
    height=100,
    placeholder="Example: Weather in Delhi and Bangalore and machine learning repositories"
)


# Example Prompts

st.markdown("Example Prompts")

col1, col2 = st.columns(2)

if col1.button("ML Repos and Multi-City Weather"):
    task = "Weather in Punjab, Delhi and Bangalore and machine learning repositories"

if col2.button("Python Repositories Only"):
    task = "Find Python repositories"

# Run Task

if st.button("Run Task"):

    if not task.strip():
        st.warning("Please enter a task.")

    else:
        with st.spinner("Processing multi-agent pipeline..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/run-task",
                    json={"task": task}
                )

                result = response.json()
                st.success("Task completed successfully")

                st.subheader("Agent Execution Flow")
                st.info("Planner generated execution plan")
                st.info("Executor executed external tools")
                st.info("Verifier validated results")

                st.divider()

               
                # Planner Output
               
                st.subheader("Planner Output")
                st.json(result.get("plan"))

                st.divider()

                
                # Executor Results
                
                st.subheader("Executor Results")

                execution_data = result.get("result", {}).get("data", {})

                # GitHub Results
                if "github" in execution_data:

                    st.markdown("GitHub Repository Results")

                    for repo in execution_data["github"]:
                        st.markdown(
                            f"**[{repo['name']}]({repo['url']})** | Stars: {repo['stars']}"
                        )
                        st.write(repo["description"])
                        st.write("---")

                # Weather Results 
                if "weather" in execution_data:

                    st.markdown("Weather Information")

                    for weather in execution_data["weather"]:

                        st.write(f"City: {weather['city']}")
                        st.write(f"Temperature: {weather['temperature']} °C")
                        st.write(f"Condition: {weather['description']}")
                        st.write(f"Humidity: {weather['humidity']} %")
                        st.write("---")

                st.divider()

                
                # Verifier Status
                
                st.subheader("Verifier Status")

                verifier_output = result.get("result", {})
                st.json(verifier_output)

                issues = verifier_output.get("issues", [])

                if issues:
                    st.warning("Issues detected:")
                    for issue in issues:
                        st.write(issue)

                st.divider()

                
                # Summary Dashboard
                
                st.subheader("Execution Summary")

                col1, col2 = st.columns(2)

                if "github" in execution_data:
                    col1.metric(
                        "Repositories Found",
                        len(execution_data["github"])
                    )

                if "weather" in execution_data:
                    col2.metric(
                        "Cities Processed",
                        len(execution_data["weather"])
                    )

            except Exception as e:
                st.error(f"Backend connection failed: {e}")

st.markdown("---")
st.caption("Built using FastAPI, Streamlit, Groq LLM and Multi-Agent Architecture")
