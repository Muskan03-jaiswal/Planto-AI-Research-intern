# summarizer agent/crew/tools/coding_agent_bridge.py
from typing import Dict
from pathlib import Path
import importlib.util, sys

class CodingAgentBridge:
    name = "code_only_generator"
    description = "Call the external CodingAgent to get code-only output. Input: {prompt:str}"

    def __init__(self, path_to_coding_agent:str):
        # Dynamically import CodingAgent from CODING AGENTS
        spec = importlib.util.spec_from_file_location(
            "codingAgentt",
            str(Path(path_to_coding_agent))
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["codingAgentt"] = mod
        spec.loader.exec_module(mod)
        self.coder = mod.CodingAgent()

    def run(self, prompt: str) -> str:
        return self.coder.process_request(prompt)
