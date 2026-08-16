from datetime import date

from pydantic import BaseModel, ConfigDict


class OpportunityBase(BaseModel):
    title: str
    company: str

    location: str | None = None
    city: str | None = None
    country: str | None = None
    remote: bool = False

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


class OpportunityResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str | None
    city: str | None
    country: str | None
    remote: bool
    url: str
    salary_min: float | None
    salary_max: float | None
    salary_currency: str | None
    date_posted: date | None
    deadline: date | None
    description: str | None
    source: str | None

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

class OpportunityListResponse(BaseModel):
    items: list[OpportunityResponse]
    page: int
    limit: int
    total: int
    pages: int

class IngestionResponse(BaseModel):
    source: str
    found: int
    created: int
    updated: int