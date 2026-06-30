import os
import pandas as pd

input_path = "outputs/fast_semantic_submission.csv"
output_path = "outputs/final_submission.csv"

df = pd.read_csv(input_path)

final = df[["candidate_id", "rank", "score", "reasoning"]].copy()

final = final.sort_values(
    by=["score", "candidate_id"],
    ascending=[False, True]
).reset_index(drop=True)

final["rank"] = final.index + 1

final.to_csv(output_path, index=False)

print("Final submission created:", output_path)
print(final.head())