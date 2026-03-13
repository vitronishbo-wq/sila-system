from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
T = TypeVar('T')

class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, db: Session, id) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, skip: int=0, limit: int=100) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> T:
        obj = self.model(**data)
        db.add(obj)
        try:
            db.commit()
            db.refresh(obj)
            return obj
        except IntegrityError:
            db.rollback()
            raise

    def save_all(self, db: Session, objects: List[T]):
        db.add_all(objects)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

    def flush(self, db: Session):
        db.flush()