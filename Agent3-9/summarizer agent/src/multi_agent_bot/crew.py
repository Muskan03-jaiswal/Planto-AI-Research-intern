# crew.py
from crewai import Crew
from tools.web_search_tool import serpapi_search  # removed leading dot for relative import if tools is in same dir

def load_crew():
    return Crew.from_yaml_files(
        agent_yaml="crew.yaml",
        task_yaml="tasks.yaml",
        tools=[serpapi_search()]
    )
