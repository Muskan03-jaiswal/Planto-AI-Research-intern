from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define prompt
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following:\n{text}"
)

# Create summarizer agent
llm = OpenAI()
summarizer = LLMChain(llm=llm, prompt=prompt)

# Run summarization
long_text = "Artificial intelligence is transforming industries by automating tasks..."
summary = summarizer.run({"text": long_text})
print("Summary:", summary)
