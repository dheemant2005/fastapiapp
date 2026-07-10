import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.job import Job
import os

load_dotenv()

COLLECTION_NAME = "job_descriptions"
VECTOR_SIZE = 384  # BGE-small outputs 384-dim vectors

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant = None
if QDRANT_URL:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

embeddings_model = TextEmbedding("BAAI/bge-small-en-v1.5")

def ensure_collection():
    if qdrant is None:
        return
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME in collections:
        info = qdrant.get_collection(COLLECTION_NAME)
        existing_size = info.config.params.vectors.size
        if existing_size != VECTOR_SIZE:
            qdrant.delete_collection(COLLECTION_NAME)
            collections = [c for c in collections if c != COLLECTION_NAME]
    if COLLECTION_NAME not in collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )

def embed_text(text: str) -> list[float]:
    vectors = embeddings_model.embed([text])
    # embeddings_model.embed returns a generator/iterator; take first item
    vec = next(vectors)
    try:
        return vec.tolist()
    except AttributeError:
        return list(vec)


async def embed_all_jobs(db: AsyncSession) -> int:
    if qdrant is None:
        return 0
    ensure_collection()
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    if not jobs:
        return 0

    points = []
    for job in jobs:
        text = f"{job.title} {job.description or ''}"
        vector = embed_text(text)
        points.append(
            PointStruct(
                id=job.id,
                vector=vector,
                payload={
                    "title": job.title,
                    "description": job.description or "",
                    "salary": job.salary,
                    "job_id": job.id,
                },
            )
        )

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


def search_jobs(query: str, top_k: int = 5) -> list[dict]:
    if qdrant is None:
        return []
    ensure_collection()
    query_vector = embed_text(query)
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    return [
        {
            "job_id": hit.payload.get("job_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description"),
            "salary": hit.payload.get("salary"),
            "score": round(hit.score, 4) if hasattr(hit, "score") else None,
        }
        for hit in getattr(results, "points", [])
    ]


def match_jobs_for_profile(skills: str, experience: str, top_k: int = 5) -> list[dict]:
    if qdrant is None:
        return []
    ensure_collection()
    profile_text = f"Skills: {skills}, Experience: {experience}"
    profile_vector = embed_text(profile_text)
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=profile_vector,
        limit=top_k,
    )
    return [
        {
            "job_id": hit.payload.get("job_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description"),
            "salary": hit.payload.get("salary"),
            "match_score": round(hit.score * 100, 2) if hasattr(hit, "score") else None,
        }
        for hit in getattr(results, "points", [])
    ]