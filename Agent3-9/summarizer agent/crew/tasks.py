from crewai import Task
from pathlib import Path

def parser_task(agent, user_input: str, prompt_path: str) -> Task:
    tmpl = Path(prompt_path).read_text(encoding="utf-8")
    return Task(
        description=tmpl + f"\n\nUser request:\n{user_input}",
        agent=agent,
        expected_output="Strict JSON with keys topic, task_type, language, constraints, tests_needed, search_queries, acceptance_criteria",
    )

def rag_task(agent, intent_json: str) -> Task:
    return Task(
        description=f"""Use WebSearchTool on each search query from this intent:
{intent_json}

Steps:
1) parse JSON.
2) for each search query, call web_search(query).
3) call rag_search.index_web_results_with_text(pages) to index all pages.
4) call rag_search.ask(intent.topic or the full user question) to get top chunks.
Return a compact JSON like:
{{"chunks":[{{"url":"...","title":"...","chunk":"..."}}, ...]}}""",
        agent=agent,
        expected_output="JSON with a 'chunks' list of source chunks."
    )

def summarize_task(agent, chunks_json: str, prompt_path: str) -> Task:
    tmpl = Path(prompt_path).read_text(encoding="utf-8")
    return Task(
        description=tmpl + f"\n\nRAG chunks JSON:\n{chunks_json}",
        agent=agent,
        expected_output="Sections: Key Facts, Caveats, Sources"
    )

def code_task(agent, intent_json: str, summary_text: str, prompt_path: str) -> Task:
    tmpl = Path(prompt_path).read_text(encoding="utf-8")
    return Task(
        description=tmpl + f"""\n\nINTENT JSON:\n{intent_json}\n\nSUMMARY:\n{summary_text}\n""",
        agent=agent,
        expected_output='JSON with "files", "readme", and "run_cmd".'
    )
