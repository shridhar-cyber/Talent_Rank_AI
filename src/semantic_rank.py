import json
import os
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

from src.config import DATA_PATH, OUTPUT_PATH, TOP_K
from src.features import build_candidate_text
from src.scoring import score_candidate


JD_TEXT = """
Senior AI Engineer - Founding Team.

We are looking for a senior AI engineer who can build intelligent candidate
discovery systems. The candidate should have experience in machine learning,
LLMs, retrieval augmented generation, semantic search, hybrid search, vector
databases, embeddings, BM25, ranking systems, learning-to-rank, evaluation
metrics like NDCG, MRR, MAP, production ML systems, APIs, MLOps, and scalable
AI products.

Preferred experience includes building recruiter-facing search, recommendation
systems, behavioral signal integration, candidate-job matching, LLM reranking,
and production deployment.
"""


def load_candidates(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Encoding job description...")
    jd_embedding = model.encode(JD_TEXT, convert_to_tensor=True)

    results = []

    for candidate in tqdm(load_candidates(DATA_PATH), desc="Semantic ranking"):
        candidate_id = candidate.get("candidate_id")

        if not candidate_id:
            continue

        candidate_text = build_candidate_text(candidate)

        if not candidate_text.strip():
            continue

        rule_score, reason = score_candidate(candidate)

        candidate_embedding = model.encode(candidate_text[:6000], convert_to_tensor=True)

        semantic_score = float(
            util.cos_sim(jd_embedding, candidate_embedding)[0][0]
        )

        semantic_score = max(0, min(semantic_score, 1))

        final_score = (
            0.55 * rule_score +
            0.45 * semantic_score
        )

        results.append({
            "candidate_id": candidate_id,
            "score": round(final_score, 4),
            "rule_score": round(rule_score, 4),
            "semantic_score": round(semantic_score, 4),
            "reasoning": reason
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    top_results = results[:TOP_K]

    for index, row in enumerate(top_results, start=1):
        row["rank"] = index

    df = pd.DataFrame(top_results)
    df = df[[
        "candidate_id",
        "rank",
        "score",
        "rule_score",
        "semantic_score",
        "reasoning"
    ]]

    os.makedirs("outputs", exist_ok=True)
    df.to_csv("outputs/semantic_submission.csv", index=False)

    print("Semantic submission created: outputs/semantic_submission.csv")
    print(df.head(10).to_string())


if __name__ == "__main__":
    main()