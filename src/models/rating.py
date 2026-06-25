from enum import Enum
from pydantic import BaseModel
from datetime import date


class RatingType(str, Enum):
    ELO = "elo"
    FIFA = "fifa"


class Rating(BaseModel):
    team_id: str
    rating_type: RatingType
    value: float
    rank: int = 0
    record_date: date | None = None
    source: str = ""
