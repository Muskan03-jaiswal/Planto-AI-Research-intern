import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

class CodingAgent:
    def __init__(self):
        """Initialize the coding agent with configuration"""
        load_dotenv()
        self.google_key = os.getenv("GEMINI_API_KEY")  # now matches .env
        self.model_name = os.getenv("MODEL", "gemini/gemini-2.0-flash")

        self.gemini_llm = LLM(
            model=self.model_name,
            api_key=self.google_key,
            temperature=0.3,
            max_tokens=None,
            top_p=0.8,
            top_k=40,
        )

        self.coder = self._create_agent()

    def _create_agent(self) -> Agent:
        return Agent(
            role="Code Generator",
            goal="Return only valid code in proper markdown code blocks without explanations or comments.",
            backstory="You are a code-only assistant.",
            llm=self.gemini_llm,
            verbose=False,
            max_iter=2,
            max_execution_time=30,
            allow_delegation=True,
            memory=False,
            system_template="""
You output ONLY code.

Rules:
1. Never write explanations, comments, or text.
2. Always wrap the entire output inside one proper markdown code block with language tag.
3. No inline code formatting.
4. No text before or after the code block.
"""
        )

    def process_request(self, user_input: str) -> str:
        task = Task(
            description=f"""
User request: "{user_input}"

Respond with ONLY the code inside a single proper markdown code block with language specified.
No explanations, no comments, no extra text.
""",
            expected_output="Only code inside a proper markdown code block.",
            agent=self.coder,
            max_execution_time=25,
        )

        crew = Crew(
            agents=[self.coder],
            tasks=[task],
            verbose=False,
            memory=False,
            cache=False,
            max_rpm=15,
            share_crew=False,
        )

        return str(crew.kickoff())
