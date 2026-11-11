from src.config import GEMINI_API_KEY
from google import genai
import json

with open("data/jd_affirm_extracted.json", "r", encoding="utf-8") as f:
    jd_data = json.load(f)

with open("data/resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)

prompt = """Extract the skills, tools, and seniority level from this resume.
Return ONLY valid JSON, no other text, in exactly this shape:
{"skills": [...], "tools": [...], "seniority": "...", "years_experience": "..."}
Resume:
""" + resume_text

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)

resume_data = json.loads(response.text)

def normalize(items):
    return set(item.strip().lower() for item in items)

jd_needed = normalize(jd_data.get("skills", []) + jd_data.get("tools", []))
resume_have = normalize(resume_data.get("skills", []) + resume_data.get("tools", []))

matched = sorted(jd_needed & resume_have)
missing = sorted(jd_needed - resume_have)
extra = sorted(resume_have - jd_needed)

match_percent = round(len(matched) / len(jd_needed) * 100, 1) if jd_needed else 0

print(f"\nMatched ({len(matched)}): {matched}")
print(f"Missing ({len(missing)}): {missing}")
print(f"Extra on resume, not asked by JD ({len(extra)}): {extra}")
print(f"Match: {match_percent}%")

report = {
    "matched": matched,
    "missing": missing,
    "extra": extra,
    "match_percent": match_percent
}

with open("data/gap_report.json", "w", encoding="utf-8") as out:
    json.dump(report, out, indent=2)

print("Saved to data/gap_report.json")
