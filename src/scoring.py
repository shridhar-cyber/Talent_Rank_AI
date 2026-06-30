from datetime import datetime

from src.features import build_candidate_text, get_years_experience


CORE_AI_SKILLS = [
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "llm", "large language model", "generative ai", "genai",
    "fine-tuning llms", "fine tuning", "computer vision"
]

RETRIEVAL_SKILLS = [
    "rag", "retrieval augmented generation", "semantic search",
    "vector database", "vector db", "embeddings", "milvus", "faiss",
    "pinecone", "qdrant", "weaviate", "elasticsearch",
    "opensearch", "haystack", "bm25", "ranking", "recommendation", "search"
]

ENGINEERING_SKILLS = [
    "python", "fastapi", "flask", "django", "docker", "kubernetes",
    "aws", "gcp", "azure", "mlops", "bentoml", "mlflow",
    "api", "microservices", "spark", "airflow", "kafka"
]

NEGATIVE_KEYWORDS = [
    "photoshop", "tailwind", "marketing", "sales", "hr recruiter",
    "graphic design", "content writing"
]


def weighted_skill_score(candidate, target_skills):
    skills = candidate.get("skills", [])
    score = 0.0
    max_possible = 18.0

    skill_aliases = {
        "llm": [
            "llm", "large language model", "fine-tuning llms",
            "fine tuning", "lora", "qlora", "rag", "genai", "generative ai"
        ],
        "nlp": [
            "nlp", "speech recognition", "tts", "text classification",
            "question answering", "sentence transformers"
        ],
        "vector": [
            "milvus", "faiss", "pinecone", "qdrant", "weaviate",
            "vector database", "embeddings", "semantic search", "haystack"
        ],
        "mlops": [
            "mlops", "bentoml", "docker", "kubernetes", "airflow",
            "kubeflow", "mlflow", "weights & biases"
        ],
        "backend": [
            "python", "fastapi", "flask", "django", "api",
            "microservices", "kafka", "spark"
        ],
        "ranking": [
            "ranking", "recommendation", "recommendation systems",
            "search", "elasticsearch", "opensearch", "bm25", "ndcg", "mrr", "map"
        ]
    }

    target_text = " ".join(target_skills).lower()

    for skill in skills:
        if not isinstance(skill, dict):
            continue

        name = str(skill.get("name", "")).lower()
        proficiency = str(skill.get("proficiency", "")).lower()
        duration = float(skill.get("duration_months", 0) or 0)
        endorsements = float(skill.get("endorsements", 0) or 0)

        matched = False

        for target in target_skills:
            target = target.lower()
            if target in name or name in target:
                matched = True

        for group, aliases in skill_aliases.items():
            if group in target_text:
                if any(alias in name for alias in aliases):
                    matched = True

        if matched:
            points = 1.0

            if proficiency == "expert":
                points += 1.5
            elif proficiency == "advanced":
                points += 1.2
            elif proficiency == "intermediate":
                points += 0.7

            if duration >= 36:
                points += 0.8
            elif duration >= 24:
                points += 0.6
            elif duration >= 12:
                points += 0.3

            if endorsements >= 40:
                points += 0.5
            elif endorsements >= 20:
                points += 0.35
            elif endorsements >= 5:
                points += 0.2

            score += points

    return min(score / max_possible, 1.0)


def experience_score(years):
    if 5 <= years <= 9:
        return 1.0
    if 4 <= years < 5:
        return 0.75
    if 9 < years <= 12:
        return 0.80
    if 2 <= years < 4:
        return 0.45
    return 0.20


def location_score(candidate):
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    country = str(profile.get("country", "")).lower()
    location = str(profile.get("location", "")).lower()
    willing_to_relocate = signals.get("willing_to_relocate", False)

    if "india" in country:
        if "pune" in location or "noida" in location:
            return 1.0
        return 0.8

    if willing_to_relocate:
        return 0.55

    return 0.15


def behavioral_score(candidate):
    signals = candidate.get("redrob_signals", {})

    score = 0.0

    if signals.get("open_to_work_flag"):
        score += 0.15

    if signals.get("verified_email"):
        score += 0.10

    if signals.get("verified_phone"):
        score += 0.10

    response_rate = float(signals.get("recruiter_response_rate", 0) or 0)
    score += min(response_rate, 1.0) * 0.20

    interview_rate = float(signals.get("interview_completion_rate", 0) or 0)
    score += min(interview_rate, 1.0) * 0.15

    acceptance_rate = float(signals.get("offer_acceptance_rate", 0) or 0)
    score += min(acceptance_rate, 1.0) * 0.10

    github_score = float(signals.get("github_activity_score", 0) or 0)
    score += min(github_score / 100, 1.0) * 0.10

    saved = float(signals.get("saved_by_recruiters_30d", 0) or 0)
    score += min(saved / 20, 1.0) * 0.10

    avg_response_time = float(signals.get("avg_response_time_hours", 999) or 999)

    if avg_response_time <= 6:
        score += 0.10
    elif avg_response_time <= 24:
        score += 0.06
    elif avg_response_time <= 72:
        score += 0.03

    return min(score, 1.0)


def recency_score(candidate):
    signals = candidate.get("redrob_signals", {})
    date_str = signals.get("last_active_date")

    if not date_str:
        return 0.3

    try:
        last_active = datetime.strptime(date_str, "%Y-%m-%d")
        current = datetime(2026, 6, 22)
        days = (current - last_active).days

        if days <= 7:
            return 1.0
        if days <= 30:
            return 0.8
        if days <= 60:
            return 0.55
        if days <= 120:
            return 0.35
        return 0.15

    except Exception:
        return 0.3


def salary_score(candidate):
    signals = candidate.get("redrob_signals", {})
    salary = signals.get("expected_salary_range_inr_lpa", {})

    min_sal = salary.get("min", 0) or 0
    max_sal = salary.get("max", 0) or 0
    avg = (float(min_sal) + float(max_sal)) / 2 if max_sal else float(min_sal)

    if 20 <= avg <= 45:
        return 1.0
    if 12 <= avg < 20:
        return 0.75
    if 45 < avg <= 60:
        return 0.65
    return 0.35


def title_score(candidate):
    profile = candidate.get("profile", {})
    title = str(profile.get("current_title", "")).lower()
    headline = str(profile.get("headline", "")).lower()
    combined = title + " " + headline

    strong_titles = [
        "senior ai engineer",
        "senior machine learning engineer",
        "senior ml engineer",
        "ai engineer",
        "machine learning engineer",
        "ml engineer",
        "applied scientist",
        "nlp engineer",
        "llm engineer",
        "deep learning engineer",
        "founding engineer"
    ]

    related_titles = [
        "data scientist",
        "backend engineer",
        "data engineer",
        "software engineer",
        "research engineer",
        "mlops engineer",
        "search engineer"
    ]

    junior_terms = ["junior", "intern", "trainee", "associate"]

    for term in junior_terms:
        if term in combined:
            return 0.35

    for title_keyword in strong_titles:
        if title_keyword in combined:
            if "senior" in combined or "lead" in combined or "principal" in combined:
                return 1.0
            return 0.85

    for title_keyword in related_titles:
        if title_keyword in combined:
            return 0.65

    return 0.3


def production_evidence_score(candidate):
    text = build_candidate_text(candidate)

    strong_terms = [
        "production",
        "deployed",
        "deployment",
        "implemented",
        "integrated",
        "built",
        "shipped",
        "customer-facing",
        "real-time",
        "pipeline",
        "system",
        "api",
        "evaluation framework",
        "monitoring",
        "latency",
        "scale",
        "load",
        "reduced",
        "improved",
        "cut",
        "optimized"
    ]

    score = 0.0

    for term in strong_terms:
        if term in text:
            score += 0.06

    return min(score, 1.0)


def negative_penalty(candidate):
    text = build_candidate_text(candidate)
    penalty = 0.0

    for word in NEGATIVE_KEYWORDS:
        if word in text:
            penalty += 0.03

    years = get_years_experience(candidate)

    if years < 2:
        penalty += 0.10

    return min(penalty, 0.25)


def seniority_penalty(candidate):
    profile = candidate.get("profile", {})
    text = build_candidate_text(candidate)

    title = str(profile.get("current_title", "")).lower()
    headline = str(profile.get("headline", "")).lower()
    combined_title = title + " " + headline

    penalty = 0.0

    junior_terms = [
        "junior", "intern", "trainee", "associate", "entry level"
    ]

    weak_production_terms = [
        "still building depth",
        "learning modern ml",
        "building competence",
        "lightweight deployment",
        "not production",
        "not from-scratch",
        "small datasets",
        "side projects"
    ]

    for term in junior_terms:
        if term in combined_title:
            penalty += 0.12

    for term in weak_production_terms:
        if term in text:
            penalty += 0.04

    return min(penalty, 0.25)


def availability_penalty(candidate):
    signals = candidate.get("redrob_signals", {})
    profile = candidate.get("profile", {})

    penalty = 0.0

    notice = float(signals.get("notice_period_days", 0) or 0)
    avg_response_time = float(signals.get("avg_response_time_hours", 0) or 0)

    if notice > 90:
        penalty += 0.08
    elif notice == 90:
        penalty += 0.04

    if avg_response_time > 120:
        penalty += 0.08
    elif avg_response_time > 72:
        penalty += 0.04

    preferred_work_mode = str(signals.get("preferred_work_mode", "")).lower()
    willing_to_relocate = signals.get("willing_to_relocate", False)
    country = str(profile.get("country", "")).lower()
    location = str(profile.get("location", "")).lower()

    if preferred_work_mode == "remote":
        if "pune" not in location and "noida" not in location and not willing_to_relocate:
            penalty += 0.06

    if "india" not in country and not willing_to_relocate:
        penalty += 0.12

    return min(penalty, 0.25)


def score_candidate(candidate):
    years = get_years_experience(candidate)

    ai = weighted_skill_score(candidate, CORE_AI_SKILLS)
    retrieval = weighted_skill_score(candidate, RETRIEVAL_SKILLS)
    engineering = weighted_skill_score(candidate, ENGINEERING_SKILLS)
    production = production_evidence_score(candidate)
    exp = experience_score(years)
    loc = location_score(candidate)
    behavior = behavioral_score(candidate)
    recency = recency_score(candidate)
    salary = salary_score(candidate)
    title = title_score(candidate)

    penalty = negative_penalty(candidate)
    penalty += seniority_penalty(candidate)
    penalty += availability_penalty(candidate)

    final_score = (
        0.22 * ai +
        0.21 * retrieval +
        0.16 * engineering +
        0.10 * production +
        0.09 * exp +
        0.07 * title +
        0.07 * behavior +
        0.03 * loc +
        0.03 * recency +
        0.02 * salary
        - penalty
    )

    final_score = max(0, min(final_score, 1))

    reason = generate_reason(
        ai, retrieval, engineering, production, exp, title,
        behavior, loc, recency, salary, penalty, years
    )

    return final_score, reason


def generate_reason(ai, retrieval, engineering, production, exp, title, behavior, loc, recency, salary, penalty, years):
    reasons = []

    if ai >= 0.6:
        reasons.append("strong AI/ML skill alignment")

    if retrieval >= 0.5:
        reasons.append("relevant retrieval/search/vector database exposure")

    if engineering >= 0.5:
        reasons.append("solid production engineering background")

    if production >= 0.5:
        reasons.append("clear evidence of shipped production ML/AI systems")

    if exp >= 0.9:
        reasons.append(f"ideal experience range for senior role ({years} years)")

    if title >= 0.85:
        reasons.append("current title matches AI/ML role")

    if behavior >= 0.7:
        reasons.append("strong hiring intent and engagement signals")

    if loc >= 0.8:
        reasons.append("location fit for India/Pune/Noida requirement")

    if recency >= 0.8:
        reasons.append("recently active profile")

    if salary >= 0.8:
        reasons.append("expected salary appears aligned")

    if penalty > 0:
        reasons.append("penalty applied for seniority, availability, or noisy signals")

    if not reasons:
        reasons.append("partial fit based on available candidate profile")

    return "; ".join(reasons)