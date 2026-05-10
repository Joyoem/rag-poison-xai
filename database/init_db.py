from pathlib import Path


def init_chroma_db(db_dir: str = "database/chroma_db_local") -> Path:
    path = Path(db_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    created = init_chroma_db()
    print(f"ChromaDB directory ready at: {created.resolve()}")
