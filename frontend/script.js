// if running locally, please use const API_BASE_URL = "const API_BASE_URL = "http://localhost:8000";

// Change this to your Render URL after deployment, e.g.
const API_BASE_URL = "https://nirmaan-interview-scorer.onrender.com";

const textarea = document.getElementById("transcript");
const scoreBtn = document.getElementById("score-btn");
const statusEl = document.getElementById("status");
const overallScoreEl = document.getElementById("overall-score");
const criteriaResultsEl = document.getElementById("criteria-results");

async function scoreTranscript() {
  const transcript = textarea.value.trim();
  if (!transcript) {
    statusEl.textContent = "Please paste a transcript before scoring.";
    return;
  }

  statusEl.textContent = "Scoring transcript...";
  overallScoreEl.textContent = "";
  criteriaResultsEl.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE_URL}/score`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        transcript: transcript,
        rubric_id: "default"
      })
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }

    const data = await res.json();

    overallScoreEl.textContent = `Overall Score: ${data.overall_score} / 100`;
    statusEl.textContent = "Scoring complete.";

    if (Array.isArray(data.criteria_scores)) {
      data.criteria_scores.forEach((crit) => {
        const card = document.createElement("div");
        card.className = "criteria-card";

        const header = document.createElement("div");
        header.className = "criteria-header";

        const name = document.createElement("div");
        name.className = "criteria-name";
        name.textContent = crit.name;

        const score = document.createElement("div");
        score.className = "criteria-score";
        score.textContent = `${crit.score} / 100`;

        header.appendChild(name);
        header.appendChild(score);

        const breakdown = document.createElement("div");
        breakdown.className = "criteria-breakdown";
        const b = crit.breakdown || {};
        breakdown.innerHTML = `
          Keyword coverage: <strong>${b.keyword_score ?? "–"}</strong> / 100<br/>
          Semantic similarity: <strong>${b.semantic_score ?? "–"}</strong> / 100<br/>
          Length adequacy: <strong>${b.length_score ?? "–"}</strong> / 100<br/>
          Weight in overall score: <strong>${b.weight ?? "–"}</strong>
        `;

        card.appendChild(header);
        card.appendChild(breakdown);

        criteriaResultsEl.appendChild(card);
      });
    }
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Error contacting scoring API. Check console.";
  }
}

scoreBtn.addEventListener("click", scoreTranscript);
 
