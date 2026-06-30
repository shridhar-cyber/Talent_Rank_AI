import json
import os
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

from src.config import DATA_PATH, TOP_K
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

CANDIDATE_POOL_SIZE = 1500


def load_candidates(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    print("Stage 1: Fast rule-based scoring...")

    rule_results = []

    for candidate in tqdm(load_candidates(DATA_PATH), desc="Rule scoring"):
        candidate_id = candidate.get("candidate_id")

        if not candidate_id:
            continue

        rule_score, reason = score_candidate(candidate)
        candidate_text = build_candidate_text(candidate)

        rule_results.append({
            "candidate_id": candidate_id,
            "rule_score": rule_score,
            "reasoning": reason,
            "candidate_text": candidate_text[:6000]
        })

    rule_results = sorted(
        rule_results,
        key=lambda x: x["rule_score"],
        reverse=True
    )[:CANDIDATE_POOL_SIZE]

    print(f"Stage 2: Semantic reranking top {CANDIDATE_POOL_SIZE} candidates...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    jd_embedding = model.encode(
        JD_TEXT,
        convert_to_tensor=True
    )

    candidate_texts = [row["candidate_text"] for row in rule_results]

    candidate_embeddings = model.encode(
        candidate_texts,
        convert_to_tensor=True,
        batch_size=64,
        show_progress_bar=True
    )

    semantic_scores = util.cos_sim(jd_embedding, candidate_embeddings)[0]

    final_results = []

    for row, semantic_score in zip(rule_results, semantic_scores):
        semantic_score = float(semantic_score)
        semantic_score = max(0, min(semantic_score, 1))

        rule_score = float(row["rule_score"])

        hidden_gem_score = 0.0

        if semantic_score >= 0.68 and rule_score <= 0.65:
            hidden_gem_score = semantic_score - rule_score

        hidden_gem_flag = hidden_gem_score >= 0.08

        final_score = (
            0.50 * rule_score +
            0.42 * semantic_score +
            0.08 * hidden_gem_score
        )

        confidence_score = (
            0.50 * final_score +
            0.25 * semantic_score +
            0.15 * min(rule_score, 1.0) +
            0.10
        )

        confidence_score = min(confidence_score, 1.0)

        reasoning = row["reasoning"]

        if hidden_gem_flag:
            reasoning += (
                "; hidden gem: strong semantic match despite lower "
                "traditional rule-based score"
            )

        final_results.append({
            "candidate_id": row["candidate_id"],
            "score": round(final_score, 4),
            "rule_score": round(rule_score, 4),
            "semantic_score": round(semantic_score, 4),
            "confidence_score": round(confidence_score, 4),
            "hidden_gem_score": round(hidden_gem_score, 4),
            "hidden_gem": hidden_gem_flag,
            "reasoning": reasoning
        })

    final_results = sorted(final_results, key=lambda x: x["score"], reverse=True)
    top_results = final_results[:TOP_K]

    for index, row in enumerate(top_results, start=1):
        row["rank"] = index

    df = pd.DataFrame(top_results)

    df = df[
        [
            "candidate_id",
            "rank",
            "score",
            "rule_score",
            "semantic_score",
            "confidence_score",
            "hidden_gem_score",
            "hidden_gem",
            "reasoning"
        ]
    ]

    os.makedirs("outputs", exist_ok=True)

    df.to_csv("outputs/fast_semantic_submission.csv", index=False)

    print("Fast semantic submission created: outputs/fast_semantic_submission.csv")
    print(df.head(10).to_string())


if __name__ == "__main__":
    main()