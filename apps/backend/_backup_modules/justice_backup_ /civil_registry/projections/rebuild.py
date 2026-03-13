from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.justice.bounded_contexts.events.models import CitizenEventModel
from app.modules.justice.bounded_contexts.projections.projectors import CitizenProjector

def rebuild_all_projections(db: Session):
    db.commit()
    query = select(CitizenEventModel).order_by(CitizenEventModel.created_at.asc())
    events = db.execute(query).scalars().all()
    projector = CitizenProjector(db)
    for event in events:
        projector.apply_event(event)
    return len(events)