from datetime import datetime

import httpx

from app.ingestion.base import OpportunitySource
from app.ingestion.location import normalize_location
from app.schemas.opportunity import OpportunityCreate


class ArbeitnowSource(OpportunitySource):

    API_URL = "https://www.arbeitnow.com/api/job-board-api"

    def fetch(self) -> list[OpportunityCreate]:
        response = httpx.get(
            self.API_URL,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        opportunities = []

        for job in data["data"]:
            created_date = datetime.fromtimestamp(
                job["created_at"]
            ).date()

            city, country = normalize_location(
                job.get("location")
            )

            opportunity = OpportunityCreate(
                title=job["title"],
                company=job["company_name"],
                location=job.get("location") or None,
                city=city,
                country=country,
                remote=job.get("remote", False),
                url=job["url"],
                salary_min=None,
                salary_max=None,
                salary_currency=None,
                date_posted=created_date,
                deadline=None,
                description=job.get("description"),
                source="Arbeitnow",
            )

            opportunities.append(opportunity)

        return opportunities


