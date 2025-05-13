import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def clean_json_block(raw):
    """
    Elimina los bloques tipo ```json ... ``` y deja solo el JSON.
    """
    cleaned = re.sub(r"^```json", "", raw.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    return cleaned.strip()

def structure_cv(raw_text):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Revolt CV App",
            },
            model="openai/gpt-4o",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Convert the following CV text into a structured JSON with:
- description (short paragraph)
- stack (list)
- experience (title, company, years, summary)
- education (degree, institution, years)

CV:
\"\"\"
{raw_text[:3000]}
\"\"\"
"""
                }
            ]
        )

        print("🔥 RAW COMPLETION:", completion)

        content = completion.choices[0].message.content.strip()
        json_string = clean_json_block(content)

        try:
            return json.loads(json_string)
        except json.JSONDecodeError as err:
            print("⚠️ JSON decode error:", err)
            print("🔍 Usando eval() como fallback.")
            return eval(json_string)

    except Exception as e:
        print("❌ OpenRouter error:", e)
        return {
            "description": "No CV content was processed.",
            "stack": [],
            "experience": [],
            "education": []
        }
