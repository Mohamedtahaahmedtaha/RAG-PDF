from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 

api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("Error: API Key not found in environment.")

OPENROUTER_MODEL =  "mistralai/mistral-7b-instruct:free" #"Qwen/Qwen-7B-Chat" 

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def ask_llm(prompt: str) -> str:
    """
    Sends the prompt/query to the configured OpenRouter LLM (Large Language Model) 
    endpoint and returns the generated textual response.
    """

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512,
        # OpenRouter sometimes requires an additional HTTP header (e.g., 'X-App-Name') 
        # to identify your application or project (Optional).
        extra_headers={
            "HTTP-Referer": "http://localhost:8000", 
            "X-Title": "PDF Extractor App",
        },
    )
    # Modifying data access in v1
    return response.choices[0].message.content