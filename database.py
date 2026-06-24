import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy_cockroachdb  # noqa: F401 - registers the CockroachDB SQLAlchemy dialect

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

def normalize_database_url(database_url: str) -> str:
    parsed = urlsplit(database_url)
    if not parsed.scheme.startswith(("postgresql", "postgres", "cockroachdb")):
        return database_url

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault("sslmode", "require")

    if parsed.hostname and "cockroachlabs.cloud" in parsed.hostname:
        if parsed.scheme.startswith("postgresql"):
            parsed = parsed._replace(scheme=parsed.scheme.replace("postgresql", "cockroachdb", 1))
        elif parsed.scheme.startswith("postgres"):
            parsed = parsed._replace(scheme=parsed.scheme.replace("postgres", "cockroachdb", 1))
        query["sslmode"] = "require"

    return urlunsplit(parsed._replace(query=urlencode(query)))

DATABASE_URL = normalize_database_url(DATABASE_URL)
print(f"Using database dialect: {urlsplit(DATABASE_URL).scheme}")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
