from src.config import GEMINI_API_KEY
from google import genai
import math
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
resume_data = json.loads(response.text)

jd_items = jd_data.get("skills", []) + jd_data.get("tools", [])
resume_items = resume_data.get("skills", []) + resume_data.get("tools", [])

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

def embed_text(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

print(f"Embedding {len(jd_items)} JD items and {len(resume_items)} resume items...")
jd_vecs = []
for item in jd_items:
    jd_vecs.append(embed_text(item))

resume_vecs = []
for item in resume_items:
    resume_vecs.append(embed_text(item))

print("Done embedding, now comparing...")

THRESHOLD = 0.65

matched = []
missing = []
details = []

for jd_item, jd_vec in zip(jd_items, jd_vecs):
    best_score = -1
    best_match = ""
    for resume_item, resume_vec in zip(resume_items, resume_vecs):
        score = cosine_similarity(jd_vec, resume_vec)
        if score > best_score:
            best_score = score
            best_match = resume_item

    is_match = best_score >= THRESHOLD
    details.append({"jd_item": jd_item, "best_match": best_match, "score": round(best_score, 3), "matched": is_match})
    print(f"{jd_item} -> {best_match} ({best_score:.3f}) {'MATCH' if is_match else 'MISSING'}")
    if is_match:
        matched.append(jd_item)
    else:
        missing.append(jd_item)

match_percent = round(len(matched) / len(jd_items) * 100, 1) if jd_items else 0
print(f"\nMatched ({len(matched)} / {len(jd_items)}): {matched}")
print(f"Missing ({len(missing)}): {missing}")
print(f"Match: {match_percent}% at threshold {THRESHOLD}")

report = {"threshold": THRESHOLD, "matched": matched, "missing": missing, "match_percent": match_percent, "details": details}
with open("data/gap_report_v2.json", "w", encoding="utf-8") as out:
    json.dump(report, out, indent=2)

print("Saved to data/gap_report_v2.json")
