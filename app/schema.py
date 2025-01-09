from pydantic import BaseModel, EmailStr
from uuid import UUID

class CreateCause(BaseModel):
    title: str
    description: str
    image_url: str

class UpdateCause(CreateCause):
    pass

class CauseResponse(CreateCause):
    id: UUID

class CreateContribution(BaseModel):
    name: str
    email: EmailStr
    amount: float

class ContributionResponse(CreateContribution):
    id: UUID
    cause_id: UUID

class MessageResponse(BaseModel):
    message: str
