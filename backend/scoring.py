from typing import Dict, Any, List

import json

_rubric_cache: Dict[str, Any] = {}


def load_rubric(path: str = "rubric_config.json") -> Dict[str, Any]:
    """
    Load rubric from JSON file with simple in-memory caching.
    """
    global _rubric_cache
    if path in _rubric_cache:
        return _rubric_cache[path]

    with open(path, "r", encoding="utf-8") as f:
        rubric = json.load(f)

    _rubric_cache[path] = rubric
    return rubric


def word_count(text: str) -> int:
    return len(text.split())


def keyword_score(text: str, keywords: List[str]) -> float:
    """
    Fraction of rubric keywords found in the transcript. [0, 1]
    """
    if not keywords:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    return hits / len(keywords)


def semantic_score(text: str, description: str) -> float:
    """
    Lightweight semantic-ish score using word overlap (no heavy ML model).
    Uses Jaccard similarity between sets of words. Returns [0, 1].
    """
    if not description.strip():
        return 0.5  # neutral baseline

    text_tokens = set(text.lower().split())
    desc_tokens = set(description.lower().split())

    if not text_tokens or not desc_tokens:
        return 0.5

    intersection = text_tokens.intersection(desc_tokens)
    union = text_tokens.union(desc_tokens)

    if not union:
        return 0.5

    return len(intersection) / len(union)


def length_score(text: str, min_words: int) -> float:
    """
    1.0 if word count >= min_words, otherwise proportional. [0, 1]
    """
    if not min_words or min_words <= 0:
        return 1.0
    wc = word_count(text)
    return min(1.0, wc / min_words)


def score_transcript(transcript: str, rubric: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core scoring logic.
    Returns a dict ready to send back via API.
    """
    transcript = transcript.strip()
    if not transcript:
        return {
            "rubric_id": rubric.get("rubric_id", "default"),
            "overall_score": 0.0,
            "criteria_scores": []
        }

    criteria_results = []
    weighted_sum = 0.0
    total_weight = 0.0

    for crit in rubric.get("criteria", []):
        cid = crit["id"]
        name = crit["name"]
        desc = crit.get("description", "")
        weight = float(crit.get("weight", 1.0))
        keywords = crit.get("keywords", [])
        min_words = crit.get("min_words", 0)

        k = keyword_score(transcript, keywords)
        s = semantic_score(transcript, desc)
        l = length_score(transcript, min_words)

        # Tunable hyperparameters (keyword, semantic, length)
        alpha, beta, gamma = 0.25, 0.55, 0.20

        combined = alpha * k + beta * s + gamma * l

        # Mild non-linear scaling to reward strong answers a bit more
        combined = 0.6 * combined + 0.4 * (combined ** 2)

        combined_100 = combined * 100.0

        criteria_results.append({
            "id": cid,
            "name": name,
            "score": round(combined_100, 2),
            "breakdown": {
                "keyword_score": round(k * 100, 1),
                "semantic_score": round(s * 100, 1),
                "length_score": round(l * 100, 1),
                "weight": weight
            }
        })

        weighted_sum += combined_100 * weight
        total_weight += weight

    overall = weighted_sum / total_weight if total_weight > 0 else 0.0

    return {
        "rubric_id": rubric.get("rubric_id", "default"),
        "overall_score": round(overall, 2),
        "criteria_scores": criteria_results
    }
