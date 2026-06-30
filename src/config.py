DATA_PATH = "data/candidates.jsonl"

OUTPUT_PATH = "outputs/submission.csv"

TOP_K = 100

TARGET_KEYWORDS = {
    "core_ai": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "llm",
        "large language model",
        "generative ai",
        "genai",
        "nlp",
        "computer vision"
    ],

    "retrieval": [
        "rag",
        "retrieval augmented generation",
        "semantic search",
        "vector database",
        "vector db",
        "embeddings",
        "faiss",
        "pinecone",
        "qdrant",
        "weaviate",
        "elasticsearch",
        "ranking",
        "recommendation",
        "search"
    ],

    "engineering": [
        "python",
        "fastapi",
        "flask",
        "django",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "mlops",
        "api",
        "microservices",
        "production"
    ],

    "evaluation": [
        "ndcg",
        "mrr",
        "map",
        "precision",
        "recall",
        "auc",
        "evaluation",
        "ranking metrics"
    ]
}