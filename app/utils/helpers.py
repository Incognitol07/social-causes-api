# app/utils/helpers.py

from fastapi import  HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.utils import logger
from app.models import Cause, Contribution


# Helper functions
def get_cause_by_id(id: UUID, db: Session):
    cause = db.query(Cause).filter(Cause.id == id).first()
    if not cause:
        logger.warning(f"No cause found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cause found with ID: {id}",
        )
    return cause

def get_contributions_by_cause_id(cause_id: UUID, db: Session):
    contributions = db.query(Contribution).filter(Contribution.cause_id == cause_id).all()
    if not contributions:
        logger.info(f"No contributions found for cause with ID: {cause_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contributions were found for cause with ID: {cause_id}",
        )
    return contributions