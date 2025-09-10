# crew/tools/compression_tool.py
from typing import List
from crewai.tools import BaseTool
import textwrap

class CompressionTool(BaseTool):
    """
    Tool to compress/shorten long text into a more compact summary.
    """

    name: str = "compression_tool"
    description: str = "Compress long text into shorter form while preserving key meaning."

    def _run(self, text: str, max_length: int = 500) -> str:
        """
        Compress text by stripping extra whitespace and truncating.
        Replace this with a more advanced summarizer if needed.
        """
        # Clean whitespace
        cleaned = " ".join(text.split())

        # Simple compression: truncate to max_length
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length] + "..."

        return cleaned
