from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app.utils import (
    logger,
    get_contributions_by_cause_id,
    get_cause_by_id
)
from app.database import get_db
from app.models import Cause, Contribution
from app.schema import (
    CreateCause,
    CreateContribution,
    CauseResponse,
    ContributionResponse,
    AllContributionResponse,
    UpdateCause,
    MessageResponse,
)

cause_router = APIRouter(prefix="/causes", tags=["Causes"])

# Routes
@cause_router.post("/", response_model=CauseResponse)
async def create_cause(create_cause: CreateCause, db: Session = Depends(get_db)):
    existing_cause = db.query(Cause).filter(
        Cause.title == create_cause.title,
        Cause.description == create_cause.description,
        Cause.image_url == create_cause.image_url,
    ).first()

    if existing_cause:
        logger.warning(f"Cause '{create_cause.title}' already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cause '{create_cause.title}' already exists",
        )

    new_cause = Cause(
        title=create_cause.title,
        description=create_cause.description,
        image_url=create_cause.image_url,
    )
    db.add(new_cause)
    db.commit()
    db.refresh(new_cause)

    logger.info(f"Created new cause with ID: {new_cause.id}")
    return new_cause


@cause_router.get("/", response_model=list[CauseResponse])
async def get_all_causes(db: Session = Depends(get_db)):
    causes = db.query(Cause).all()
    if not causes:
        logger.warning("No causes found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No causes found",
        )
    logger.info(f"Retrieved {len(causes)} causes")
    return causes


@cause_router.get("/{id}", response_model=CauseResponse)
async def get_cause(id: UUID, db: Session = Depends(get_db)):
    cause = get_cause_by_id(id, db)
    logger.info(f"Retrieved cause with ID: {id}")
    return cause


@cause_router.put("/{id}", response_model=CauseResponse)
async def update_cause(id: UUID, update_cause: UpdateCause, db: Session = Depends(get_db)):
    cause = get_cause_by_id(id, db)

    # Update fields
    updated_data = update_cause.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(cause, key, value)

    db.commit()
    db.refresh(cause)
    logger.info(f"Updated cause with ID: {id}")
    return cause


@cause_router.delete("/{id}", response_model=MessageResponse)
async def delete_cause(id: UUID, db: Session = Depends(get_db)):
    cause = get_cause_by_id(id, db)
    db.delete(cause)
    db.commit()
    logger.info(f"Deleted cause with ID: {id}")
    return {"message": f"Deleted cause with ID: {id}"}


@cause_router.post("/{id}/contribute", response_model=ContributionResponse)
async def contribute_to_cause(id: UUID, contribution: CreateContribution, db: Session = Depends(get_db)):
    cause = get_cause_by_id(id, db)

    new_contribution = Contribution(
        name=contribution.name,
        email=contribution.email,
        amount=contribution.amount,
        cause_id=cause.id,
    )
    db.add(new_contribution)
    db.commit()
    db.refresh(new_contribution)

    logger.info(f"Added contribution of {contribution.amount} to cause ID: {id}")
    return new_contribution


@cause_router.get("/{id}/contribute", response_model=AllContributionResponse)
async def get_cause_contribution(id: UUID, db: Session = Depends(get_db)):
    cause = get_cause_by_id(id, db)
    contributions = get_contributions_by_cause_id(id, db)

    total_amount = sum(contribution.amount for contribution in contributions)
    logger.info(f"Total Contributions for cause ID {id}: {len(contributions)}, Total Amount: {total_amount}")

    return {
        "contribution_count": len(contributions),
        "total_amount": total_amount,
        "contributions": contributions,
    }
