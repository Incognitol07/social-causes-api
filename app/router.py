# app/router.py

from fastapi import (
    APIRouter, 
    HTTPException, 
    status,
    Depends
)
from uuid import UUID
from sqlalchemy.orm import Session
from app.utils import logger
from app.database import get_db
from app.models import Cause, Contribution
from app.schema import ( 
    CreateCause, 
    CreateContribution, 
    CauseResponse, 
    ContributionResponse,
    UpdateCause,
    MessageResponse
)

cause_router = APIRouter(prefix="/causes", tags=["Causes"])

@cause_router.post("/", response_model=CauseResponse)
async def create_cause(
    create_cause: CreateCause,
    db: Session = Depends(get_db)
):
    cause = db.query(Cause).filter(
        Cause.title == create_cause.title, 
        Cause.description == create_cause.description,
        Cause.image_url == create_cause.image_url
        ).first()

    if cause:
        logger.warning(f"Cause {cause.title} already found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cause {cause.title} already found"
        )
    
    new_cause = Cause(
        title = create_cause.title,
        description = create_cause.description,
        image_url = create_cause.image_url
    )
    db.add(new_cause)
    db.commit()
    db.refresh(new_cause)
    
    return new_cause

@cause_router.get("/", response_model=list[CauseResponse])
async def get_all_causes(
    db: Session = Depends(get_db)
):
    causes = db.query(Cause).all()

    if not causes:
        logger.warning("No causes were found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No causes found"
        )
    
    return causes

@cause_router.get("/{id}", response_model=CauseResponse)
async def get_cause(
    id: UUID,
    db: Session = Depends(get_db)
):
    cause = db.query(Cause).filter(Cause.id == id).first()

    if not cause:
        logger.warning(f"No cause was found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cause was found with ID: {id}"
        )
    
    return cause

@cause_router.put("/{id}", response_model=CauseResponse)
async def update_cause(
    id: UUID,
    update_cause: UpdateCause,
    db: Session = Depends(get_db)
):
    cause = db.query(Cause).filter(Cause.id == id).first()

    if not cause:
        logger.warning(f"No cause was found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cause was found with ID: {id}"
        )
    
    # Update the cause fields with the provided data
    for key, value in update_cause.model_dump(exclude_unset=True).items():
        setattr(cause, key, value)

    db.commit()
    db.refresh(cause)
    
    return cause

@cause_router.delete("/{id}", response_model=MessageResponse)
async def delete_cause(
    id: UUID,
    db: Session = Depends(get_db)
):
    cause = db.query(Cause).filter(Cause.id == id).first()

    if not cause:
        logger.warning(f"No cause was found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No cause was found with ID: {id}"
        )
    
    db.delete(cause)
    db.commit()

    return {"message":f"Deleted cause with ID: {id}"}


@cause_router.post("/{id}/contribute", response_model=ContributionResponse)
async def contribute_to_cause(
    id: UUID,
    contribution: CreateContribution,
    db: Session = Depends(get_db)
):
    cause = db.query(Cause).filter(Cause.id == id).first()

    if not cause:
        logger.warning(f"No cause was found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No cause was found with ID: {id}"
        )
    
    new_contribution = Contribution(
        name = contribution.name,
        email = contribution.email,
        amount = contribution.amount,
        cause_id = cause.id
    )
    db.add(new_contribution)
    db.commit()
    db.refresh(new_contribution)
    
    return new_contribution