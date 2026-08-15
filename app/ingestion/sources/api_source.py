# import httpx

# from app.ingestion.base import OpportunitySource
# from app.schemas.opportunity import OpportunityCreate


# class APIOpportunitySource(OpportunitySource):

#     def fetch(self) -> list[OpportunityCreate]:
#         response = httpx.get(
#             "https://example.com/api/jobs",
#             timeout=10,
#         )

#         response.raise_for_status()

#         data = response.json()

#         opportunities = []

#         for job in data:
#             opportunity = OpportunityCreate(
#                 title=job["title"],
#                 company=job["company"],
#                 location=job.get("location"),
#                 city=job.get("city"),
#                 country=job.get("country"),
#                 url=job["url"],
#                 salary_min=job.get("salary_min"),
#                 salary_max=job.get("salary_max"),
#                 salary_currency=job.get("salary_currency"),
#                 date_posted=job.get("date_posted"),
#                 deadline=job.get("deadline"),
#                 description=job.get("description"),
#                 source="API",
#             )

#             opportunities.append(opportunity)

#         return opportunities