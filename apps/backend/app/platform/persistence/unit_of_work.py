from __future__ import annotations


class UnitOfWork:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
            return False
        self.db.commit()
        return False
