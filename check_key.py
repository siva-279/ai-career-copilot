from src.config import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-3.5-flash-lite", contents="Say hello"
)
print(response.text)
