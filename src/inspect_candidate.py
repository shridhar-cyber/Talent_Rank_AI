import json
import sys
from pprint import pprint

from src.config import DATA_PATH


def find_candidate(candidate_id):
    count = 0

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            count += 1
            candidate = json.loads(line)

            if candidate.get("candidate_id") == candidate_id:
                print(f"Found after scanning {count} candidates")
                return candidate

    print(f"Scanned {count} candidates")
    return None


def main():
    print("Inspect candidate script started")

    if len(sys.argv) < 2:
        print("Usage: python -m src.inspect_candidate CAND_0024990")
        return

    candidate_id = sys.argv[1].strip()
    print(f"Searching for candidate: {candidate_id}")

    candidate = find_candidate(candidate_id)

    if candidate is None:
        print("Candidate not found")
        return

    print("\nPROFILE")
    pprint(candidate.get("profile", {}))

    print("\nTOP SKILLS")
    skills = candidate.get("skills", [])
    skills = sorted(
        skills,
        key=lambda x: (
            x.get("endorsements", 0),
            x.get("duration_months", 0)
        ),
        reverse=True
    )
    pprint(skills[:20])

    print("\nCAREER HISTORY")
    pprint(candidate.get("career_history", [])[:3])

    print("\nREDROB SIGNALS")
    pprint(candidate.get("redrob_signals", {}))


if __name__ == "__main__":
    main()