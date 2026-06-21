from app.db.database import SessionLocal


def test_database_session_created():
    db = SessionLocal()

    try:
        assert db is not None
    finally:
        db.close()