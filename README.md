# Nirmaan AI – Interview Transcript Scorer

This project automatically scores a candidate's **self-introduction interview transcript** against a rubric inspired by Nirmaan AI’s case-study.

It uses a hybrid approach:

- ✅ **Rule-based features** (keywords, length)
- ✅ **Semantic similarity** with sentence embeddings
- ✅ **Weighted rubric criteria** (Content & Structure, Speech Rate, Language & Grammar, Clarity, Engagement)

---

## 🧱 Tech Stack

**Backend**

- Python 3.10+
- FastAPI (REST API)
- `sentence-transformers` (`all-MiniLM-L6-v2`) for semantic similarity
- `scikit-learn` for cosine similarity

**Frontend**

- Static HTML, CSS, vanilla JavaScript
- Calls the FastAPI backend via a simple `/score` endpoint

**Hosting (planned / recommended)**

- Backend: **Render** (free Web Service)
- Frontend: **Vercel** (free static site)

---

## 📊 Scoring Logic (High Level)

For each rubric criterion (e.g., *Content & Structure*, *Engagement*), we compute:

1. **Keyword Score** – coverage of important rubric keywords in the transcript.
2. **Semantic Score** – cosine similarity between:
   - the transcript,
   - the criterion description (from `rubric_config.json`)
3. **Length Score** – how well the transcript meets a minimum word count.

Each component is in **[0, 1]** and combined as:

```text
combined = 0.25 * keyword_score
         + 0.55 * semantic_score
         + 0.20 * length_score

combined = 0.6 * combined + 0.4 * (combined ** 2)
