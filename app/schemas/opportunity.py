from datetime import date

from pydantic import BaseModel, ConfigDict


class OpportunityBase(BaseModel):
    title: str
    company: str

    location: str | None = None
    city: str | None = None
    country: str | None = None

    url: str
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None

    date_posted: date | None = None
    deadline: date | None = None

    description: str | None = None
    source: str | None = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityResponse(OpportunityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class OpportunityUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    city: str | None = None
    country: str | None = None

    url: str | None = None

    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None

    date_posted: date | None = None
    deadline: date | None = None

    description: str | None = None
    source: str | None = None