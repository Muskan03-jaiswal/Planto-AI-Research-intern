#Coding Agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define prompt
prompt = PromptTemplate(
    input_variables=["task"],
    template="Write Python code to accomplish the following task:\n{task}"
)

# Create coding agent
llm = OpenAI()
coder = LLMChain(llm=llm, prompt=prompt)

# Run coding task
task_description = "Sort a list of numbers in ascending order"
code_output = coder.run({"task": task_description})
print("Generated Code:\n", code_output)
