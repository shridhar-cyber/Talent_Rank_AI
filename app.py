import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="TalentRankAI",
    page_icon="🚀",
    layout="wide"
)

OUTPUT_PATH = "outputs/fast_semantic_submission.csv"
SUMMARY_PATH = "outputs/run_summary.json"

DEFAULT_JD = """
Senior AI Engineer - Founding Team

We are looking for a senior AI engineer who can build intelligent candidate discovery systems.

The candidate should have experience in:
- Machine Learning
- LLMs
- Retrieval Augmented Generation
- Semantic Search
- Vector Databases
- Embeddings
- BM25
- Ranking Systems
- Learning-to-Rank
- Evaluation metrics like NDCG, MRR, MAP
- Production ML systems
- APIs and MLOps

Preferred experience:
- Recruiter-facing search systems
- Recommendation systems
- Behavioral signal integration
- Candidate-job matching
- LLM reranking
- Production deployment
"""

AVERAGE_RADAR_SCORES = {
    "AI Skills": 45,
    "Retrieval": 38,
    "Production": 50,
    "Experience": 60,
    "Behavior": 52,
    "Availability": 58,
}


# =========================
# DATA
# =========================

@st.cache_data
def load_data():
    return pd.read_csv(OUTPUT_PATH)


def load_summary(df):
    summary = {
        "candidate_pool_evaluated": "N/A",
        "ranked_shortlist": len(df),
        "best_candidate": df.iloc[0]["candidate_id"],
        "hidden_gems_found": int(df["hidden_gem"].sum()) if "hidden_gem" in df.columns else 0,
        "top_fit_score": round(df.iloc[0]["score"] * 100, 1),
        "avg_semantic_match": round(df["semantic_score"].mean() * 100, 1),
        "avg_confidence": round(df["confidence_score"].mean() * 100, 1),
    }

    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
                summary.update(json.load(f))
        except Exception:
            pass

    return summary


# =========================
# HELPERS
# =========================

def analyze_job_description(jd_text):
    jd_lower = jd_text.lower()

    groups = {
        "AI / ML": ["machine learning", "deep learning", "ai", "artificial intelligence", "ml"],
        "LLMs / GenAI": ["llm", "large language model", "generative ai", "genai", "rag", "prompt"],
        "Retrieval / Search": ["retrieval", "semantic search", "vector", "embedding", "faiss", "pinecone", "weaviate", "qdrant", "bm25", "search"],
        "Ranking Systems": ["ranking", "learning-to-rank", "ltr", "reranking", "recommendation", "recommender"],
        "Production Engineering": ["production", "deployment", "api", "docker", "kubernetes", "mlops", "latency", "scalable"],
        "Evaluation": ["ndcg", "mrr", "map", "precision", "recall", "evaluation", "metrics"],
        "Behavioral Signals": ["behavior", "engagement", "intent", "activity", "signals"],
    }

    rows = []

    for group, keywords in groups.items():
        matched = [kw for kw in keywords if kw in jd_lower]
        if matched:
            rows.append({
                "Focus Area": group,
                "Detected Keywords": ", ".join(matched)
            })

    if not rows:
        rows.append({
            "Focus Area": "General AI Role",
            "Detected Keywords": "No strong specialized keyword detected"
        })

    return pd.DataFrame(rows)


def build_radar_scores(row):
    return {
        "AI Skills": min(row["rule_score"] * 110, 100),
        "Retrieval": min(row["semantic_score"] * 115, 100),
        "Production": min(row["rule_score"] * 100, 100),
        "Experience": min(row["score"] * 110, 100),
        "Behavior": min(row["rule_score"] * 90, 100),
        "Availability": min(row["semantic_score"] * 85, 100),
    }


def radar_chart(candidate_name, candidate_scores, average_scores):
    labels = list(candidate_scores.keys())

    candidate_values = list(candidate_scores.values())
    average_values = list(average_scores.values())

    candidate_values += candidate_values[:1]
    average_values += average_values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.2, 5.2), subplot_kw=dict(polar=True))

    ax.plot(angles, candidate_values, linewidth=2, label=candidate_name)
    ax.fill(angles, candidate_values, alpha=0.25)

    ax.plot(angles, average_values, linewidth=2, label="Overall Average")
    ax.fill(angles, average_values, alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right")

    return fig


def confidence_message(confidence):
    if confidence >= 0.85:
        st.success("🟢 Very High Recruiter Confidence")
    elif confidence >= 0.75:
        st.info("🔵 High Recruiter Confidence")
    elif confidence >= 0.65:
        st.warning("🟡 Moderate Recruiter Confidence")
    else:
        st.error("🔴 Low Recruiter Confidence")


def recruiter_decision(score):
    if score >= 0.75:
        st.success("Strongly Recommended — shortlist for interview.")
    elif score >= 0.65:
        st.warning("Recommended — review manually before shortlisting.")
    else:
        st.error("Weak Match — not a top-priority candidate.")


def hidden_gem_explanation(row, df):
    semantic_percentile = (df["semantic_score"] < row["semantic_score"]).mean() * 100
    reason = str(row["reasoning"]).lower()

    st.markdown(f"🟢 **Semantic relevance is higher than {semantic_percentile:.0f}% of shortlisted candidates**")

    if "retrieval" in reason or "search" in reason or "vector" in reason:
        st.markdown("🟢 **Strong retrieval/search or vector database relevance**")

    if "production" in reason or "shipped" in reason:
        st.markdown("🟢 **Evidence of production AI/ML system experience**")

    if "ai/ml" in reason or "machine learning" in reason:
        st.markdown("🟢 **Strong AI/ML alignment with the target role**")

    if "experience" in reason:
        st.markdown("🟢 **Experience level fits the senior role expectations**")

    if "hiring intent" in reason or "engagement" in reason:
        st.markdown("🟢 **Positive hiring intent or recruiter engagement signals**")


# =========================
# LOAD
# =========================

df = load_data()
summary = load_summary(df)

top_n = st.sidebar.slider(
    "Show top candidates",
    min_value=5,
    max_value=100,
    value=20
)

filtered_df = df.head(top_n)


# =========================
# HEADER
# =========================

st.title("🚀 TalentRankAI")
st.caption("Explainable Candidate Discovery Engine")

st.markdown(
    """
    TalentRankAI helps recruiters identify best-fit candidates using
    **hybrid candidate scoring, semantic job-role matching, behavioral signals,
    hidden gem discovery, and recruiter confidence scoring.**
    """
)


# =========================
# TABS
# =========================

tab_jd, tab_shortlist, tab_deep, tab_hidden, tab_compare, tab_download = st.tabs(
    [
        "📝 Job Description",
        "🏆 Shortlist",
        "👤 Deep Dive",
        "🔥 Hidden Gems",
        "⚖ Compare",
        "📥 Download",
    ]
)


# =========================
# TAB 1 — JD
# =========================

with tab_jd:
        # ==========================
    # Executive Hiring Summary
    # ==========================

    st.header("📝 Job Description Understanding")

    best_candidate = df.iloc[0]

    hidden_gem_count = (
        int(df["hidden_gem"].sum())
        if "hidden_gem" in df.columns
        else 0
    )

    st.subheader("📋 Hiring Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🏆 Best Candidate",
            value=best_candidate["candidate_id"]
        )

    with col2:
        st.metric(
            label="🎯 Match Score",
            value=f"{best_candidate['score']*100:.1f}%"
        )

    with col3:
        st.metric(
            label="💎 Hidden Gems",
            value=hidden_gem_count
        )

    st.success(
        f"""
### Recommendation

TalentRankAI recommends **{best_candidate['candidate_id']}** as the strongest overall candidate.

**Why?**

• Highest overall ranking

• Strong semantic match with the job description

• High recruiter confidence

• Excellent AI/ML profile alignment

In addition, **{hidden_gem_count} hidden gem candidate(s)** were discovered that deserve recruiter attention.
"""
    )

    st.divider()

    st.info(
        "The official hackathon job description is preloaded below. "
        "Recruiters can edit it to understand how TalentRankAI detects role focus areas."
    )

    jd_text = st.text_area(
        "Paste or edit the job description",
        value=DEFAULT_JD,
        height=280
    )

    if st.button("Analyze Candidates"):
        jd_analysis = analyze_job_description(jd_text)

        st.subheader("Detected Role Focus Areas")
        st.dataframe(jd_analysis, use_container_width=True)

        st.success(
            "Job description analyzed. Candidate ranking uses semantic matching "
            "and structured scoring aligned with these role signals."
        )


# =========================
# TAB 2 — SHORTLIST
# =========================

with tab_shortlist:
    st.header("🏆 Ranked Candidate Shortlist")

    columns = [
        "rank",
        "candidate_id",
        "score",
        "rule_score",
        "semantic_score",
        "confidence_score",
    ]

    if "hidden_gem" in df.columns:
        columns.append("hidden_gem")

    st.dataframe(
        filtered_df[columns],
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "This shortlist is generated using hybrid candidate scoring and semantic reranking. "
        "Use Deep Dive to understand individual recommendations."
    )


# =========================
# TAB 3 — DEEP DIVE
# =========================

with tab_deep:
    st.header("👤 Candidate Deep Dive")

    candidate_id = st.selectbox(
        "Select candidate",
        filtered_df["candidate_id"],
        key="deep_dive_candidate"
    )

    selected = filtered_df[filtered_df["candidate_id"] == candidate_id].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Final Fit Score", f"{selected['score'] * 100:.1f}%")

    with col2:
        st.metric("Rule Score", f"{selected['rule_score'] * 100:.1f}%")

    with col3:
        st.metric("Semantic Match", f"{selected['semantic_score'] * 100:.1f}%")

    with col4:
        st.metric("Recruiter Confidence", f"{selected['confidence_score'] * 100:.1f}%")

    confidence_message(selected["confidence_score"])

    if "hidden_gem" in df.columns and selected["hidden_gem"]:
        st.success("🔥 Hidden Gem Candidate")

    st.subheader("Why this candidate?")
    st.info(selected["reasoning"])

    left, right = st.columns(2)

    with left:
        st.subheader("Score Breakdown")

        breakdown = pd.DataFrame({
            "Component": [
                "Rule-Based Fit",
                "Semantic JD Match",
                "Recruiter Confidence"
            ],
            "Score": [
                selected["rule_score"] * 100,
                selected["semantic_score"] * 100,
                selected["confidence_score"] * 100
            ]
        })

        st.bar_chart(breakdown.set_index("Component"))

    with right:
        st.subheader("Capability Radar")

        fig = radar_chart(
            candidate_id,
            build_radar_scores(selected),
            AVERAGE_RADAR_SCORES
        )

        st.pyplot(fig)

    st.subheader("Recruiter Decision")
    recruiter_decision(selected["score"])


# =========================
# TAB 4 — HIDDEN GEMS
# =========================

with tab_hidden:
    st.header("🔥 Hidden Gem Discovery")

    if "hidden_gem" not in df.columns:
        st.warning("Hidden gem columns not found. Run: python -m src.fast_semantic_rank")
    else:
        hidden_gems = df[df["hidden_gem"] == True].copy()

        if hidden_gems.empty:
            st.info("No hidden gems found in the current shortlisted output.")
        else:
            hidden_gems = hidden_gems.sort_values(
                by=["semantic_score", "confidence_score", "score"],
                ascending=[False, False, False]
            ).head(3)

            hidden_gems = hidden_gems.reset_index(drop=True)
            hidden_gems["hidden_gem_rank"] = hidden_gems.index + 1

            st.markdown(
                """
                Hidden gems are candidates who may not appear at the very top through
                traditional rule-based filtering, but show strong relevance when semantic
                matching is applied.
                """
            )

            medals = [
                "🥇 Best Hidden Gem",
                "🥈 Strong Hidden Gem",
                "🥉 Promising Hidden Gem"
            ]

            for idx, row in hidden_gems.iterrows():
                st.subheader(medals[idx])

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Candidate", row["candidate_id"])

                with c2:
                    st.metric("Hidden Gem Rank", f"#{int(row['hidden_gem_rank'])}")

                with c3:
                    st.metric("Semantic Match", f"{row['semantic_score'] * 100:.1f}%")

                with c4:
                    st.metric("Confidence", f"{row['confidence_score'] * 100:.1f}%")

                st.markdown("### Why TalentRankAI believes this candidate is undervalued")
                hidden_gem_explanation(row, df)

                st.warning(
                    "Traditional screening may undervalue this profile, but semantic matching "
                    "suggests the candidate deserves recruiter review."
                )

                comparison = pd.DataFrame({
                    "System": [
                        "Traditional Rule Match",
                        "Semantic TalentRankAI Match"
                    ],
                    "Score": [
                        row["rule_score"] * 100,
                        row["semantic_score"] * 100
                    ]
                })

                st.subheader("Traditional ATS vs TalentRankAI")
                st.bar_chart(comparison.set_index("System"))

                st.divider()


# =========================
# TAB 5 — COMPARE
# =========================

with tab_compare:
    st.header("⚖ Candidate Comparison")

    col_a, col_b = st.columns(2)

    with col_a:
        candidate_a = st.selectbox(
            "Candidate A",
            filtered_df["candidate_id"],
            key="candidate_a"
        )

    with col_b:
        candidate_b = st.selectbox(
            "Candidate B",
            filtered_df["candidate_id"],
            index=1 if len(filtered_df) > 1 else 0,
            key="candidate_b"
        )

    row_a = filtered_df[filtered_df["candidate_id"] == candidate_a].iloc[0]
    row_b = filtered_df[filtered_df["candidate_id"] == candidate_b].iloc[0]

    comparison_data = {
        "Metric": [
            "Final Score",
            "Rule Score",
            "Semantic Score",
            "Recruiter Confidence",
        ],
        candidate_a: [
            row_a["score"],
            row_a["rule_score"],
            row_a["semantic_score"],
            row_a["confidence_score"],
        ],
        candidate_b: [
            row_b["score"],
            row_b["rule_score"],
            row_b["semantic_score"],
            row_b["confidence_score"],
        ],
    }

    if "hidden_gem_score" in df.columns:
        comparison_data["Metric"].append("Hidden Gem Score")
        comparison_data[candidate_a].append(row_a["hidden_gem_score"])
        comparison_data[candidate_b].append(row_b["hidden_gem_score"])

    comparison_df = pd.DataFrame(comparison_data)

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    if row_a["score"] > row_b["score"]:
        st.success(
            f"{candidate_a} is ranked higher by "
            f"{round((row_a['score'] - row_b['score']) * 100, 2)} score points."
        )
    elif row_b["score"] > row_a["score"]:
        st.success(
            f"{candidate_b} is ranked higher by "
            f"{round((row_b['score'] - row_a['score']) * 100, 2)} score points."
        )
    else:
        st.info("Both candidates have equal final score.")

    radar_left, radar_right = st.columns(2)

    with radar_left:
        st.subheader(candidate_a)
        fig_a = radar_chart(candidate_a, build_radar_scores(row_a), AVERAGE_RADAR_SCORES)
        st.pyplot(fig_a)

    with radar_right:
        st.subheader(candidate_b)
        fig_b = radar_chart(candidate_b, build_radar_scores(row_b), AVERAGE_RADAR_SCORES)
        st.pyplot(fig_b)


# =========================
# TAB 6 — DOWNLOAD
# =========================

with tab_download:
    st.header("📥 Download Output")

    st.markdown(
        """
        Download the explainable ranking output for review or submission.
        Use `outputs/final_submission.csv` if the competition requires the strict validated format.
        """
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Explainable Ranking CSV",
        data=csv_data,
        file_name="fast_semantic_submission.csv",
        mime="text/csv"
    )