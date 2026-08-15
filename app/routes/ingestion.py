from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.ingestion.service import ingest_opportunities
from app.ingestion.sources.mock import MockOpportunitySource
from app.schemas.opportunity import IngestionResponse
from app.ingestion.sources.arbeitnow import ArbeitnowSource


router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
)


@router.post("/mock", response_model=IngestionResponse)
def run_mock_ingestion(
    db: Session = Depends(get_db),
):
    source = MockOpportunitySource()

    result = ingest_opportunities(
        source=source,
        db=db,
    )

    return result

@router.post("/arbeitnow", response_model=IngestionResponse)
def run_arbeitnow_ingestion(
    db: Session = Depends(get_db),
):
    source = ArbeitnowSource()

    result = ingest_opportunities(
        source=source,
        db=db,
    )

    return result