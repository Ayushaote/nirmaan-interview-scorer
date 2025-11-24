# Nirmaan AI – Interview Transcript Scorer

A prototype web app that scores a candidate’s **self-introduction interview transcript** using a rubric-based approach that combines:

- Rule-based checks (keywords, content coverage, length)
- NLP-based semantic similarity (sentence embeddings)
- Weighted rubric aggregation to produce a final **0–100 score**

Built as part of the **Nirmaan AI internship case study**.

---

## 1. Project Summary

The app:

1. Accepts a transcript string (pasted into a UI text box).
2. Computes **per-criterion scores** using the given rubric (Excel).
3. Uses three approaches together:
   - **Rule-based**: keyword presence, exact matches, minimum word count.
   - **NLP-based**: semantic similarity between transcript and rubric descriptions.
   - **Weighted scoring**: combines signals with criterion weights to produce a normalized 0–100 final score.
4. Displays:
   - Overall score,
   - Per-criterion scores,
   - Basic feedback metrics (keyword coverage, semantic similarity, length).

There are **two versions** of the system:

- **Phase 1 – Full HTML/JS Frontend + FastAPI Backend (Heavy, but accurate)**  
  This is the version you should run **locally**.
- **Phase 2 – Hugging Face + Gradio UI (Lightweight deployment)**  
  Optional demo to show deployment and constraints.

---

## 2. Repository Structure

```text
.
├── backend/                     # Phase 1 backend (run this locally)
│   ├── main.py                  # FastAPI app (entrypoint)
│   ├── scoring.py               # Scoring logic (keywords + semantic similarity)
│   ├── rubric_config.json       # Rubric: criteria, weights, keywords, min word counts
│   └── requirements.txt         # Backend dependencies (torch, transformers, etc.)
│
├── frontend/                    # Phase 1 frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── huggingface_app/             # Phase 2: Gradio UI + lightweight backend (optional)
│   ├── app.py
│   ├── scoring.py
│   └── rubric_config.json
│
└── README.md                    # This file
```
If folder names differ slightly in the repo, they will still follow this backend/frontend separation.

---

## 3. How to Run the App Locally (Phase 1 – Recommended)

### 3.1 Prerequisites

- Python 3.9+
- Node.js (only if you want to use a local HTTP server for the frontend; otherwise, opening index.html in the browser is enough for basic testing)
- Git (to clone repository)

### 3.2 Clone the Repository
```
git clone https://github.com/Ayushaote/nirmaan-interview-scorer.git
cd nirmaan-interview-scorer
```

### 3.3 Set Up and Run the Backend (FastAPI)
1. Go to the backend folder:
```
cd backend
```
2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
   - Windows:
```
venv\Scripts\activate
```
   - macOS/Linux:
```
source venv/bin/activate
```
4. Install dependencies:
```
pip install -r requirements.txt
```
  This will install:
- fastapi, uvicorn
- sentence-transformers, torch
- scikit-learn, numpy, etc.

5. Run the backend server:
```
uvicorn main:app --reload
```
You should see something like:
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
6. Open API docs (optional, to test backend alone):
- Visit: http://127.0.0.1:8000/docs
- You can try the POST /score endpoint by sending:
```
  {
  "transcript": "Hello, my name is ...",
  "rubric_id": "default"
  }
```
### 3.4 Run the Frontend (HTML/CSS/JS)
1. In a new terminal window/tab (with the backend still running), go to the frontend folder:
```
cd frontend
```
2. Easiest option: open index.html directly in the browser
- Double-click index.html, or
- Right-click → “Open with” → your browser.

3. In the UI:
- Paste a self-introduction transcript in the text area.
- Click “Score Transcript”.
- The frontend will send a POST request to:
   `http://127.0.0.1:8000/score`
- The right-hand panel shows:
   - Overall score
   - Per-criterion scoring tiles
   - Keyword/semantic/length breakdowns

You now have the full Phase 1 system running locally:
Vanilla HTML/CSS/JS frontend + FastAPI backend + transformer-based scoring.

---

## 4. Deployed Link (Phase 2 – Optional Demo)
Because Phase 1 uses heavy libraries (PyTorch, SentenceTransformers), the backend could not reliably run on Render free tier (512 MB RAM). The frontend successfully deployed to Vercel, but the backend crashed during model loading.

To still demonstrate deployment skills, I built a Phase 2 version that uses the same rubric but a lighter scoring approach and moved hosting to Hugging Face Spaces.

- Frontend (Vercel):
Deployed static UI adapted from the original frontend.

- Backend + UI (Hugging Face Space – Gradio):
[HuggingFace](https://huggingface.co/spaces/vitamin-c/Nirmaan-internship-project)

This Gradio-based version:
- Uses a similar scoring pipeline (rule-based + semantic features).
- Is optimized for CPU and tighter memory.
- Serves as a public demo of the idea, while the local Phase 1 remains the more powerful model.

---

## 5. Scoring Formula & Logic (Description)

The scoring logic lives in backend/scoring.py and uses the rubric defined in backend/rubric_config.json.

### 5.1 Per-Criterion Calculation
For each criterion (e.g., Content & Structure, Clarity, Engagement), we compute:

1. Keyword Score (k)
  - Let K be the list of rubric keywords for that criterion.
  - Score = fraction of keywords present in the transcript.
  - Range: [0, 1].

2. Semantic Score (s)
  - Encode transcript and criterion description using sentence-transformers/all-MiniLM-L6-v2.
  - Compute cosine similarity between embeddings.
  - Map from [-1, 1] to [0, 1] via:
   $s = \frac{\mathrm{cosine\_sim} + 1}{2}$
3. Length Score (l)
  - min_words defined per criterion in the rubric.
  - If word_count >= min_words → 1.0
  - Else → word_count / min_words.
  - Range: [0, 1].
4. Combined Criterion Score (c)
Example weighting (tunable, but follows rubric intent):
```
alpha = 0.2   # keyword importance
beta  = 0.6   # semantic importance
gamma = 0.2   # length importance

base = alpha * k + beta * s + gamma * l
c = base ** 0.8   # small non-linear transform to spread scores
```
 - c is in [0, 1], then multiplied by 100 for display.

### 5.2 Final Overall Score
Each criterion has a weight in rubric_config.json (e.g., Content & Structure might have 0.3, Clarity 0.2, etc.).

$Overall Score = \frac{\sum_{i=1}^{n} (criterian\_score_i * weight_i)}{\sum_{i=1}^{n} weight_i}$

where each criterion_score_i is in [0, 100].
This satisfies the requirement of “description of scoring formula”.

---

## 6. Phase 1 vs Phase 2 – What Changed and Why
Phase 1 – Local Full Version (What You Run)
  - Frontend: HTML + CSS + Vanilla JS (Vercel-ready)
  - Backend: FastAPI + SentenceTransformers
  - Pros:
    - Better semantic understanding of the transcript.
    - Flexible rubric-aware scoring.
  - Cons:
    - Heavy dependencies → Render free tier ran out of memory.

Phase 2 – Hugging Face + Gradio (Public Demo)
  - UI: Gradio interface (no separate JS frontend required).
  - Backend: Same core scoring.py and rubric_config.json idea, but optimized.
  - Pros:
    - Easy to host on Hugging Face Spaces.
    - Nice demo interface to share link.
  - Cons:
    - Slightly simplified scoring to fit resource limits.

This two-phase approach shows both:
  - Full engineering pipeline (Phase 1),
  - Practical deployment trade-offs (Phase 2).

---

## 7. Submission Checklist (Mapping to Instructions)
From the problem statement’s Submission instructions:

1. Create a public GitHub repository

  - ✅ Source code included (frontend + backend).
  - ✅ requirements.txt in backend/.
  - ✅ This README.md with run instructions + scoring formula.
  - ✅ Detailed local deployment steps (Section 3).

2. Deployed link (optional but strongly encouraged)

  - ✅ Hugging Face Space link provided.
  - ✅ Frontend also deployed on Vercel for demonstration.

3. Provide exact steps to run locally in document format

  - ✅ Section 3 provides step-by-step commands.

4. Record a screen video showing the app running code
  - To be submitted as a short screen recording:
    - Start backend (uvicorn main:app --reload)
    - Open frontend
    - Paste sample transcript
    - Show scores updating

---

## 8. Author

#### Ayush Aote
##### Final-Year B.Tech Student | Machine Learning & NLP Enthusiast

