from src.config import GEMINI_API_KEY
from google import genai
import math
import json

with open("data/jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

words = jd_text.split()

chunks = []
current = []
for word in words:
    current.append(word)
    if len(current) >= 100:
        chunks.append(" ".join(current))
        current = []
if current:
    chunks.append(" ".join(current))

print(f"JD has {len(words)} words, split into {len(chunks)} chunks")

client = genai.Client(api_key=GEMINI_API_KEY)

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

embeddings = []
for chunk in chunks:
    embeddings.append(embed_text(chunk))
    print(f"Embedded chunk, {len(embeddings[-1])} numbers")

question = "What skills does this job need?"
query_vec = embed_text(question)

scored = []
for i, vec in enumerate(embeddings):
    score = cosine_similarity(query_vec, vec)
    scored.append((score, i))
    print(f"Chunk {i} similarity to question: {score:.3f}")

scored.sort(reverse=True)
top_3 = scored[:3]

print("Top 3 chunks:")
for score, i in top_3:
    print(f"  Chunk {i} score {score:.3f}")

context = ""
for score, i in top_3:
    context += chunks[i] + "\n\n"

prompt = """Answer ONLY from the context below. If the answer is not in the context, say you don't know.
Return ONLY valid JSON, no other text, in exactly this shape:
{"skills": [...], "tools": [...], "seniority": "...", "years_experience": "..."}
Context:
""" + context + "\nQuestion: " + question

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)

data = json.loads(response.text)
with open("data/jd_affirm_rag.json", "w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print("Saved to data/jd_affirm_rag.json")