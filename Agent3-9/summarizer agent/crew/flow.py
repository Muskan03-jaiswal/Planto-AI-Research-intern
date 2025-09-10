# crew/flow.py
import json
from pathlib import Path
from crewai import Crew, Process
from crew.agents import (
    make_parser_agent,
    make_rag_agent,
    make_summarizer_agent,
    make_coder_agent,
)
from crew.tasks import parser_task, rag_task, summarize_task, code_task
from crew.tools.code_writer_tool import CodeWriterTool

# Folder containing prompt templates
PROMPTS = Path(__file__).parent / "prompts"


def run_pipeline(user_request: str):
    """Orchestrates the multi-agent pipeline: Parser → RAG → Summarizer → Coder."""

    # 1. Build agents
    parser = make_parser_agent()
    from pathlib import Path
    ragger = make_rag_agent(store_path=str(Path(".memory") / "vs")) 
    summarizer = make_summarizer_agent()
    coder = make_coder_agent()

    # 2. Parser Task
    t_parse = parser_task(parser, user_request, str(PROMPTS / "parser.md"))
    parse_out = Crew(
        agents=[parser],
        tasks=[t_parse],
        process=Process.sequential,
    ).kickoff().raw

    # Try parsing JSON intent
    try:
        intent = json.loads(parse_out)
    except Exception:
        start, end = parse_out.find("{"), parse_out.rfind("}")
        intent = json.loads(parse_out[start:end + 1])
    intent_json_str = json.dumps(intent, ensure_ascii=False, indent=2)

    # 3. RAG Task
    t_rag = rag_task(ragger, intent_json_str)
    rag_out = Crew(
        agents=[ragger],
        tasks=[t_rag],
        process=Process.sequential,
    ).kickoff().raw

    # 4. Summarization Task
    t_sum = summarize_task(summarizer, rag_out, str(PROMPTS / "summarizer.md"))
    summary = Crew(
        agents=[summarizer],
        tasks=[t_sum],
        process=Process.sequential,
    ).kickoff().raw

    # 5. Code Generation Task
    t_code = code_task(coder, intent_json_str, summary, str(PROMPTS / "coder.md"))
    code_json = Crew(
        agents=[coder],
        tasks=[t_code],
        process=Process.sequential,
    ).kickoff().raw

    # 6. Handle code saving
    try:
        payload = json.loads(code_json)
        saved_path = payload.get("save_path")
        if not saved_path and "files" in payload:
            saved_path = CodeWriterTool().run(payload["files"])
            payload["save_path"] = saved_path
        final = payload
    except Exception:
        final = {"raw": code_json}

    return {
        "intent": intent,
        "summary": summary,
        "result": final,
    }
