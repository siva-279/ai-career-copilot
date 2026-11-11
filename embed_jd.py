from src.config import GEMINI_API_KEY
from google import genai
import math

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

embeddings = []
for i, chunk in enumerate(chunks):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )
    vec = response.embeddings[0].values
    embeddings.append(vec)
    print(f"Chunk {i}: {len(vec)} numbers, starts with: {chunk[:60]}...")

query = "Python"
query_response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)
query_vec = query_response.embeddings[0].values

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

best_idx = 0
best_score = -1
for i, vec in enumerate(embeddings):
    score = cosine_similarity(query_vec, vec)
    print(f"Chunk {i} similarity to 'Python': {score:.3f}")
    if score > best_score:
        best_score = score
        best_idx = i

print(f"\nChunk {best_idx} is the most similar to '{query}' (score {best_score:.3f})")
print(chunks[best_idx][:300])
