from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "anemia.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"