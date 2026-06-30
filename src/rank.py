import os
import pandas as pd
from tqdm import tqdm

from src.config import DATA_PATH, OUTPUT_PATH, TOP_K
from src.utils import load_jsonl
from src.scoring import score_candidate


def main():
    results = []

    for candidate in tqdm(load_jsonl(DATA_PATH), desc="Scoring candidates"):
        candidate_id = candidate.get("candidate_id")

        if not candidate_id:
            continue

        score, reason = score_candidate(candidate)

        results.append({
            "candidate_id": candidate_id,
            "score": round(score, 4),
            "reasoning": reason
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    top_results = results[:TOP_K]

    for index, row in enumerate(top_results, start=1):
        row["rank"] = index

    df = pd.DataFrame(top_results)
    df = df[["candidate_id", "rank", "score", "reasoning"]]

    os.makedirs("outputs", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Submission created successfully: {OUTPUT_PATH}")
    print(df.head(10))


if __name__ == "__main__":
    main()