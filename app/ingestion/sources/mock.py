from app.ingestion.base import OpportunitySource
from app.schemas.opportunity import OpportunityCreate


class MockOpportunitySource(OpportunitySource):

    def fetch(self) -> list[OpportunityCreate]:
        return [
            OpportunityCreate(
                title="Software Developer Intern",
                company="Apple",
                location="Toronto, ON",
                city="Toronto",
                country="Canada",
                url="https://example.com/apple-intern",
                salary_min=30,
                salary_max=38,
                salary_currency="CAD",
                date_posted="2026-08-15",
                deadline="2026-09-15",
                description="Software development internship.",
                source="Mock Source",
            ),
            OpportunityCreate(
                title="Backend Developer Intern",
                company="Shopify",
                location="Ottawa, ON",
                city="Ottawa",
                country="Canada",
                url="https://example.com/shopify-intern",
                salary_min=28,
                salary_max=35,
                salary_currency="CAD",
                date_posted="2026-08-14",
                deadline="2026-09-10",
                description="Backend engineering internship.",
                source="Mock Source",
            ),
            OpportunityCreate(
                title="Software Engineering Intern",
                company="Microsoft",
                location="Redmond, WA",
                city="Redmond",
                country="USA",
                url="https://example.com/microsoft-intern",
                salary_min=35,
                salary_max=45,
                salary_currency="USD",
                date_posted="2026-08-13",
                deadline="2026-09-20",
                description="Software engineering internship.",
                source="Mock Source",
            ),
        ]


