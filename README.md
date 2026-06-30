# 🚀 TalentRankAI

### Intelligent Candidate Discovery Engine

> Built for the Data & AI Challenge – Intelligent Candidate Discovery Track

---

# The Problem

Recruiters today face a difficult challenge.

A single job posting can attract thousands of candidate profiles. Traditional Applicant Tracking Systems (ATS) typically rely on keyword matching to shortlist candidates.

While this approach is fast, it often misses highly relevant candidates simply because they describe their experience differently from the job description.

As a result:

* Strong candidates are overlooked.
* Hidden talent remains undiscovered.
* Recruiters spend significant time manually reviewing profiles.
* Hiring decisions become less efficient.

The challenge is no longer finding candidates.

The challenge is finding the **right candidates**.

---

# Our Solution

TalentRankAI is an AI-powered candidate discovery engine that helps recruiters identify the most relevant candidates by combining:

* Structured profile analysis
* Behavioral signals
* Semantic understanding
* Hidden gem discovery
* Explainable AI

Instead of asking:

> "Does this candidate contain the right keywords?"

TalentRankAI asks:

> "Does this candidate actually have the skills, experience, and potential required for this role?"

---

# What Makes TalentRankAI Different?

Most hiring systems focus on filtering.

TalentRankAI focuses on discovery.

### Traditional ATS

* Keyword-based filtering
* Limited contextual understanding
* Misses semantically relevant candidates
* Provides little explanation for rankings

### TalentRankAI

* Understands candidate meaning, not just keywords
* Uses semantic matching to identify relevant expertise
* Discovers hidden talent
* Integrates behavioral signals
* Provides explainable recommendations
* Helps recruiters make faster and better decisions

---

# How TalentRankAI Works

## Step 1 — Profile Understanding

The system analyzes multiple candidate attributes including:

* Skills
* Experience
* Career history
* Education
* Certifications
* Current role
* Behavioral activity signals

This creates a structured representation of each candidate.

---

## Step 2 — Hybrid Candidate Scoring

Candidates are evaluated using:

* AI/ML skill alignment
* Retrieval and search expertise
* Production AI experience
* Career progression
* Experience relevance
* Recruiter engagement signals
* Hiring intent indicators

This generates an initial candidate ranking.

---

## Step 3 — Semantic Understanding

Traditional keyword matching has limitations.

For example:

Candidate A:

> Built retrieval systems using vector databases.

Candidate B:

> Developed AI-powered search platforms using embeddings and ranking pipelines.

Although both candidates possess similar expertise, a traditional ATS may rank them differently.

TalentRankAI uses transformer embeddings to understand the meaning behind candidate profiles and identify semantically relevant expertise.

This allows the system to surface candidates whose capabilities match the role even when exact keywords are missing.

---

## Step 4 — Hidden Gem Discovery

One of the biggest challenges in recruiting is identifying strong candidates that traditional filtering systems fail to recognize.

TalentRankAI actively searches for these candidates.

A Hidden Gem is a candidate who:

* Demonstrates strong semantic relevance
* Possesses valuable experience
* May not rank highly through conventional filtering

Rather than simply flagging these candidates, TalentRankAI explains:

* Why they were surfaced
* What strengths they possess
* Why recruiters should review them

This transforms hiring from filtering into talent discovery.

---

## Step 5 — Recruiter Confidence Score

Each recommendation includes a Recruiter Confidence Score.

This score helps recruiters quickly understand how strongly the system believes a candidate matches the target role.

The score is derived from:

* Final fit score
* Semantic relevance
* Structured profile signals
* Overall candidate strength

---

# System Architecture

![Architecture](screenshots/architecture.png)

---

# Dashboard Features

## 🏆 Ranked Candidate Shortlist

Displays the most relevant candidates with:

* Final Fit Score
* Semantic Match Score
* Recruiter Confidence Score
* Hidden Gem Indicators

![Shortlist](screenshots/shortlist.png)

---

## 👤 Candidate Deep Dive

Provides detailed explanations for every recommendation including:

* Candidate reasoning
* Score breakdown
* Capability radar chart
* Recruiter confidence
* Final recommendation

![Deep Dive](screenshots/deep_dive.png)

---

## 📊 Capability Radar Charts

TalentRankAI visualizes candidate strengths across multiple dimensions:

* AI Skills
* Retrieval & Search Expertise
* Production Experience
* Career Experience
* Behavioral Signals
* Availability

This enables recruiters to quickly understand candidate capabilities relative to the broader talent pool.

---

## 🔥 Hidden Gem Discovery

Highlights candidates who may be overlooked by traditional ranking systems but demonstrate strong semantic relevance and role fit.

For each hidden gem, TalentRankAI explains:

* Why the candidate is undervalued
* What strengths make them relevant
* Why recruiters should consider them

![Hidden Gems](screenshots/hidden_gems.png)

---

## ⚖ Candidate Comparison

Allows recruiters to compare candidates side-by-side using:

* Final Fit Score
* Semantic Match
* Recruiter Confidence
* Capability Radar Charts

This helps recruiters make more informed shortlisting decisions.

![Comparison](screenshots/comparison.png)

---

# Technology Stack

* Python
* Pandas
* NumPy
* Sentence Transformers
* Streamlit
* Matplotlib
* tqdm

---

# Project Structure

```text
TalentRankAI/
│
├── src/
│   ├── scoring.py
│   ├── features.py
│   ├── fast_semantic_rank.py
│   ├── inspect_candidate.py
│   └── config.py
│
├── outputs/
│   ├── fast_semantic_submission.csv
│   └── final_submission.csv
│
├── screenshots/
│   ├── architecture.png
│   ├── shortlist.png
│   ├── deep_dive.png
│   ├── hidden_gems.png
│   └── comparison.png
│
├── app.py
├── make_final_submission.py
├── validate_submission.py
├── requirements.txt
└── README.md
```

---

# How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate rankings:

```bash
python -m src.fast_semantic_rank
```

Create final submission:

```bash
python make_final_submission.py
```

Launch dashboard:

```bash
streamlit run app.py
```

Validate submission:

```bash
python validate_submission.py outputs/final_submission.csv
```

---

# Future Enhancements

* Learning-to-Rank models using recruiter feedback
* Personalized ranking strategies
* Conversational recruiter assistant
* Graph-based candidate relationship modeling
* Real-time recruiter feedback loops

---

# Impact

TalentRankAI helps recruiters:

* Discover stronger candidates faster
* Identify hidden talent
* Reduce manual screening effort
* Improve shortlist quality
* Make explainable hiring decisions

---

# Final Thought

Hiring is not a keyword matching problem.

It is a talent discovery problem.

TalentRankAI was built to help recruiters spend less time searching and more time discovering exceptional candidates.
