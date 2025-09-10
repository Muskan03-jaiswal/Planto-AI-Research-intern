# crew/tools/code_writer_tool.py
import os
import uuid
from typing import List, Dict, Optional
from crewai.tools import BaseTool
from crew.config import OUTPUT_DIR


class CodeWriterTool(BaseTool):
    name: str = "code_writer"
    description: str = "Write code files to disk. Input: {files:[{path:str, content:str}], session_id?:str}"

    def _run(self, files: List[Dict[str, str]], session_id: Optional[str] = None) -> str:
        """
        Writes multiple files to disk inside OUTPUT_DIR/<session_id>.
        Returns the folder path containing the written files.
        """
        sid = session_id or str(uuid.uuid4())[:8]
        base = os.path.join(OUTPUT_DIR, sid)
        os.makedirs(base, exist_ok=True)

        for f in files:
            path = os.path.join(base, f["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(f["content"])

        return base
