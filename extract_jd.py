from src.config import GEMINI_API_KEY
from google import genai
import json

with open("data/jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)

prompt = """Extract the skills, tools, and seniority level from this job description.
Return ONLY valid JSON, no other text, in exactly this shape:
{"skills": [...], "tools": [...], "seniority": "...", "years_experience": "..."}
Job description:
""" + jd_text

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)

data = json.loads(response.text)
with open("data/jd_affirm_extracted.json", "w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print("Saved to data/jd_affirm_extracted.json")
from src.config import GEMINI_API_KEY
from google import genai
import json

with open("data/jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)

prompt = """Extract the skills, tools, and seniority level from this job description.
Return ONLY valid JSON, no other text, in exactly this shape:
{"skills": [...], "tools": [...], "seniority": "...", "years_experience": "..."}
Job description:
""" + jd_text

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)

data = json.loads(response.text)
with open("data/jd_affirm_extracted.json", "w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print("Saved to data/jd_affirm_extracted.json")
