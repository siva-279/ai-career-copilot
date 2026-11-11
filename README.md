\# AI Career Copilot



I built this because I was applying to a lot of jobs and reading every job description by hand. It was slow, and I couldn't tell quickly if I actually matched a role or not.



So I made a small tool for myself. Paste a job description, it tells you the skills, tools, and seniority it wants, and what you're missing compared to my resume.



\## What it does right now



1\. Reads a JD from data/jd.txt and pulls out skills, tools, seniority as JSON

2\. Splits the JD into chunks and turns each chunk into embeddings

3\. Asks a question, finds the 3 most similar chunks, and answers only from those chunks

4\. Compares the JD against my resume and prints matched, missing, and extra



I tested it on one real JD: Affirm, Machine Learning Engineer II (Underwriting ML), Remote US.



\## How I built it



I did it in small slices, Nov 4 to Nov 11, 2026. Each slice was 45 minutes or less.



Slice 0: Get a free Gemini key and make one call. It said hello back.

Slice 1: One JD in, JSON out. Affirm JD, 390 words.

Slice 2: Split that JD into 4 chunks of 100 words, embed each chunk. Each vector is 3072 numbers.

Slice 3: Ask "What skills does this job need?", retrieve top 3 chunks, generate the answer from only those.

Slice 4: Compare JD vs my resume. Exact match was 8.3%. Matched: machine learning, python. Missing: spark, pytorch, lightgbm, xgboost, mlflow, and 17 more.



\## What went wrong



A lot, and I kept it in because that's how I learned it:



\- gemini-2.0-flash gave 404, retired. gemini-3.8-flash gave 503, overloaded. I ended up on gemini-3.5-flash-lite.

\- text-embedding-004 gave 404, not supported for embed. I switched to gemini-embedding-001.

\- In Slice 3, the seniority came back as "I don't know". That was actually correct. The chunk with the job title wasn't in the top 3 retrieved, so it refused to guess instead of making it up.

\- The 8.3% match in Slice 4 is too harsh. It compares exact words. MLOps and "model productionization" mean the same thing but count as different. I'm fixing that with semantic matching using the embeddings from Slice 2.



\## How to run it



I use Windows, PowerShell, Python 3.12.



python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt



Make a .env file in the project root with your own key. Don't paste the key anywhere else.

GEMINI\_API\_KEY=your\_key\_here



Then:

python check\_key.py

python extract\_jd.py

python embed\_jd.py

python rag\_jd.py

python gap\_check.py



You need a free key from Google AI Studio. No card needed.



\## What I would fix next



\- Chunk by paragraph, not by 100 words. Right now chunks split mid-sentence.

\- Use semantic matching for the gaps, not exact words. I started that in gap\_check\_v2.py.

\- Retrieve top 3 is fine for a short JD, but for a long one I'd want to test top 4 or 5.



\## Files



check\_key.py - Slice 0 test, asks Gemini to say hello

extract\_jd.py - Slice 1, JD to JSON

embed\_jd.py - Slice 2, chunk and embed

rag\_jd.py - Slice 3, retrieve top 3 and generate

gap\_check.py - Slice 4, JD vs resume, exact match

data/jd.txt - the Affirm JD I tested with

data/resume.txt - my resume in text form, short version



