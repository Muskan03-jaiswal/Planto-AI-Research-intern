from crewai import Crew
from crew.tools.web_search_tool import WebSearchTool

def load_crew():
    return Crew.from_yaml_files(
        agent_yaml="crew.yaml",
        task_yaml="tasks.yaml",
        tools=[WebSearchTool()]
    )
