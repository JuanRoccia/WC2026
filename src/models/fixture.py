from datetime import datetime

from pydantic import BaseModel


class MatchResult(BaseModel):
    home_goals: int
    away_goals: int


class FixtureContext(BaseModel):
    home_unavailable_players: int = 0
    away_unavailable_players: int = 0
    home_unavailable_attack_impact: float = 0.0
    away_unavailable_attack_impact: float = 0.0
    home_unavailable_defense_impact: float = 0.0
    away_unavailable_defense_impact: float = 0.0
    is_neutral_site: bool = False


class Fixture(BaseModel):
    id: str
    group_name: str
    home_team_id: str
    away_team_id: str
    home_team_name: str = ""
    away_team_name: str = ""
    kickoff: datetime | None = None
    venue: str = ""
    is_neutral: bool = False
    result: MatchResult | None = None
    is_played: bool = False
    context: FixtureContext = FixtureContext()
