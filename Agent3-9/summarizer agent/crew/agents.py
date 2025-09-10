from crewai import Agent
from crew.config import MODEL, CREW_VERBOSE
from crew.tools.web_search_tool import serpapi_search
from crew.tools.rag_tool import RAGTool
from crew.tools.web_search_tool import WebSearchTool
from crew.tools.code_writer_tool import CodeWriterTool
from crew.tools.coding_agent_bridge import CodingAgentBridge
from crew.tools.compression_tool import CompressionTool
from crew.tools.code_writer_tool import CodeWriterTool
CODE_ONLY = CodingAgentBridge(
    path_to_coding_agent="C:/Users/hp/Documents/multi-agent-projects/CODING AGENTS/src/codingagent1/codingAgentt.py"
)



def make_compression_agent():
    return Agent(
        role="Compressor",
        goal="Reduce and compress long text into shorter summaries.",
        backstory="Expert at compressing and summarizing verbose information.",
        tools=[CompressionTool()],
        **COMMON
    )


# All agents share the same model via LiteLLM
COMMON = dict(
    llm=MODEL,
    verbose=CREW_VERBOSE,
    allow_delegation=False,
)


def make_supervisor_agent():
    return Agent(
        role="Root Agent",
        goal="Plan and orchestrate Parser → RAG → Compression → Summarizer → Coder and deliver final bundle.",
        backstory="Experienced tech lead who coordinates specialists efficiently.",
        tools=[WebSearchTool(), RAGTool(store_path=".memory"), CodeWriterTool()],
        **COMMON
    )

def make_parser_agent():
    return Agent(
        role="Parser Agent",
        goal="Turn user text into structured intent JSON",
        backstory="Expert product analyst who writes crisp, strict JSON schemas.",
        tools=[],  # pure reasoning
        **COMMON
    )

def make_rag_agent(store_path: str):
    return Agent(
        role="Retriever/RAG Agent",
        goal="Search web and perform dense retrieval using Gemini embeddings.",
        backstory="A relentless researcher skilled at finding reliable sources.",
        tools=[serpapi_search(), RAGTool(store_path=store_path)],
        **COMMON
    )

def make_summarizer_agent():
    return Agent(
        role="Compressor/Summarizer",
        goal="Reduce to only actionable key facts with citations.",
        backstory="Technical editor who hates fluff and keeps only signal.",
        tools=[],  # pure reasoning
        **COMMON
    )

def make_coder_agent():
    return Agent(
        role="Coding/Problem Solver",
        goal="Write clean, working code that satisfies acceptance criteria.",
        backstory="Seasoned software engineer with a bias for simplicity.",
        tools=[CodeWriterTool()],
        **COMMON
    )

