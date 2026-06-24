import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

def normalize_postgres_ssl(database_url: str) -> str:
    parsed = urlsplit(database_url)
    if not parsed.scheme.startswith(("postgresql", "postgres", "cockroachdb")):
        return database_url

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault("sslmode", "require")

    if parsed.hostname and "cockroachlabs.cloud" in parsed.hostname and "sslrootcert" not in query:
        query["sslrootcert"] = "system"

    return urlunsplit(parsed._replace(query=urlencode(query)))

DATABASE_URL = normalize_postgres_ssl(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
