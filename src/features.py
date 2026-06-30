from src.utils import safe_get, normalize_text


def build_candidate_text(candidate):
    profile = safe_get(candidate, ["profile"], {})
    career_history = safe_get(candidate, ["career_history"], [])
    education = safe_get(candidate, ["education"], [])
    skills = safe_get(candidate, ["skills"], [])
    certifications = safe_get(candidate, ["certifications"], [])
    redrob_signals = safe_get(candidate, ["redrob_signals"], {})

    text_parts = [
        normalize_text(profile),
        normalize_text(career_history),
        normalize_text(education),
        normalize_text(skills),
        normalize_text(certifications),
        normalize_text(redrob_signals),
    ]

    return " ".join(text_parts)


def get_years_experience(candidate):
    profile = safe_get(candidate, ["profile"], {})
    years = profile.get("years_of_experience", 0)

    try:
        return float(years)
    except:
        return 0.0


def keyword_score(text, keywords):
    score = 0

    for keyword in keywords:
        if keyword.lower() in text:
            score += 1

    return score