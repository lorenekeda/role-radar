import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import (OpportunityCreate, 
                                     OpportunityListResponse, 
                                     OpportunityResponse, 
                                     OpportunityUpdate,
                                     )


router = APIRouter(
    prefix="/opportunities",
    tags=["opportunities"],
)


@router.post("/", response_model=OpportunityResponse)
def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
):
    db_opportunity = Opportunity(**opportunity.model_dump())

    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)

    return db_opportunity


@router.get("/", response_model=OpportunityListResponse)
def get_opportunities(
    country: str | None = None,
    company: str | None = None,
    source: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("date_posted"),
    order: str = Query("desc"),
    db: Session = Depends(get_db),
):
    query = db.query(Opportunity)

    if country:
        query = query.filter(Opportunity.country == country)

    if company:
        query = query.filter(Opportunity.company == company)

    if source:
        query = query.filter(Opportunity.source == source)

    sort_fields = {
        "date_posted": Opportunity.date_posted,
        "salary_min": Opportunity.salary_min,
        "salary_max": Opportunity.salary_max,
        "company": Opportunity.company,
        "title": Opportunity.title,
    }

    if sort_by not in sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field: {sort_by}",
        )

    sort_column = sort_fields[sort_by]

    if order == "asc":
        query = query.order_by(sort_column.asc())
    elif order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'",
        )

    total = query.count()

    offset = (page - 1) * limit

    opportunities = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = math.ceil(total / limit)

    return {
        "items": opportunities,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
    }

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
):
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id
    ).first()

    if opportunity is None:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found",
        )

    return opportunity

@router.put("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: int,
    opportunity_data: OpportunityUpdate,
    db: Session = Depends(get_db),
):
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id
    ).first()

    if opportunity is None:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found",
        )

    update_data = opportunity_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(opportunity, field, value)

    db.commit()
    db.refresh(opportunity)

    return opportunity

@router.delete("/{opportunity_id}")
def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
):
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id
    ).first()

    if opportunity is None:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found",
        )

    db.delete(opportunity)
    db.commit()

    return {"message": "Opportunity deleted successfully"}