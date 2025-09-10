# import argparse
# from crew.flow import run_pipeline
# from crewai import Crew

# if __name__ == "__main__":
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--ask", required=True, help="User question / request")
#     args = ap.parse_args()
#     out = run_pipeline(args.ask)
#     print("\n=== INTENT ===\n", out["intent"])
#     print("\n=== SUMMARY ===\n", out["summary"])
#     print("\n=== RESULT ===\n", out["result"])
#     if isinstance(out["result"], dict) and out["result"].get("save_path"):
#         print("\nFiles written to:", out["result"]["save_path"])

# crew = Crew.from_yaml('crew.yaml')
# crew.kickoff()
import os, json
from crew.agents import make_parser_agent, make_supervisor_agent, make_summarizer_agent, make_coder_agent, make_compression_agent
from crew.tools.rag_tool import RAGTool
from crew.tools.compression_tool import CompressionTool
from crewai import Task, Crew

os.environ.setdefault("GEMINI_API_KEY", "<PUT_YOURS>")
os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"
# Agents
parser = make_parser_agent()
rag     = make_supervisor_agent()   # includes RAGTool & CodeWriterTool
compress= make_compression_agent()
summar  = make_summarizer_agent()
coder   = make_coder_agent()

# Tools are attached inside agents; ensure vector store exists
_ = RAGTool(store_path=".memory")

# Tasks
parse_user_request = Task(
  description="Parse user input into JSON {intent, targets, acceptance}.",
  agent=parser, expected_output="JSON"
)
retrieve_and_rag = Task(
  description="Use RAG to fetch top relevant chunks for the bundle.query.",
  agent=rag, expected_output="JSON with retrieval.top_chunks"
)
compress_prompt = Task(
  description="Compress retrieved chunks into {compressed.prompt} within budget.",
  agent=compress, expected_output="JSON with {prompt, kept, dropped}"
)
summarize_results = Task(
  description="Produce a short plan and acceptance checks from compressed prompt.",
  agent=summar, expected_output="plan + acceptance in JSON"
)
write_code = Task(
  description="Generate code using either coder_agent or code_only_generator tool.",
  agent=coder, expected_output="files JSON (path, content)"
)

crew = Crew(
  agents=[parser, rag, compress, summar, coder],
  tasks=[parse_user_request, retrieve_and_rag, compress_prompt, summarize_results, write_code],
  verbose=True
)

if __name__ == "__main__":
  user_input = "Fix the memory leak in server.cpp and add a unit test."
  res = crew.kickoff(inputs={"user_input": user_input})
  print(res)
