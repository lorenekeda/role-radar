from abc import ABC, abstractmethod

from app.schemas.opportunity import OpportunityCreate


class OpportunitySource(ABC):
    @abstractmethod
    def fetch(self) -> list[OpportunityCreate]:
        """Fetch opportunities from this source."""
        pass