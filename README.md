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
