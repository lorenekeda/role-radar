import logging
from sqlalchemy.orm import Session

from app.ingestion.base import OpportunitySource
from app.models.opportunity import Opportunity

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def ingest_opportunities(
    source: OpportunitySource,
    db: Session,
) -> dict:
    logger.info("Starting ingestion from %s", source.__class__.__name__)

    opportunities = source.fetch()

    logger.info("Found %d opportunities", len(opportunities))

    created_count = 0
    updated_count = 0

    for opportunity_data in opportunities:
        existing = (
            db.query(Opportunity)
            .filter(Opportunity.url == opportunity_data.url)
            .first()
        )

        if existing:
            for field, value in opportunity_data.model_dump().items():
                setattr(existing, field, value)

            updated_count += 1

            logger.info(
                "Updated existing opportunity: %s",
                opportunity_data.url,
            )

            continue

        opportunity = Opportunity(
            **opportunity_data.model_dump()
        )

        db.add(opportunity)
        created_count += 1

    db.commit()

    logger.info(
        "Ingestion complete: %d created, %d skipped",
        created_count,
        updated_count,
    )

    return {
    "source": source.__class__.__name__,
    "found": len(opportunities),
    "created": created_count,
    "updated": updated_count,
    }
