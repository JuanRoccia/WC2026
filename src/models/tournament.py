from enum import Enum
from pydantic import BaseModel


class KnockoutStage(str, Enum):
    ROUND_OF_32 = "round_of_32"
    ROUND_OF_16 = "round_of_16"
    QUARTERFINALS = "quarterfinals"
    SEMIFINALS = "semifinals"
    FINAL = "final"
    CHAMPION = "champion"


class TeamTournamentProbability(BaseModel):
    team_id: str
    team_name: str = ""
    group_name: str = ""
    win_group_p: float = 0.0
    advance_p: float = 0.0
    round_of_32_p: float = 0.0
    round_of_16_p: float = 0.0
    quarterfinals_p: float = 0.0
    semifinals_p: float = 0.0
    final_p: float = 0.0
    champion_p: float = 0.0
    expected_points: float = 0.0
    most_common_position: str = "group_stage"


class GroupTableEntry(BaseModel):
    team_id: str
    team_name: str = ""
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0


class GroupTable(BaseModel):
    group_name: str
    entries: list[GroupTableEntry] = []


class TournamentProjection(BaseModel):
    simulation_count: int = 10000
    seed: int = 2026
    team_probabilities: list[TeamTournamentProbability] = []
    group_tables: list[GroupTable] = []
    most_likely_champion: str = ""
    most_likely_semifinalists: list[str] = []
