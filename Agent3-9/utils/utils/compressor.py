import os
import requests

def compress_text(documents, query):
    """
    Summarizes retrieved documents using Gemini 2.0 Flash via OpenRouter API directly.
    Takes a list of LangChain Document objects and a query string.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from environment variables.")

    # Combine document contents
    context_text = "\n".join([doc.page_content for doc in documents])
    prompt = f"Summarize the following text in relation to the query: '{query}'\n\n{context_text}"

    # API request setup
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    # Send request to OpenRouter
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"[Error contacting OpenRouter API] {str(e)}"
