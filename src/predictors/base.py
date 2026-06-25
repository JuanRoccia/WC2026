from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.models.fixture import Fixture, FixtureContext
from src.models.rating import Rating
from src.models.prediction import MatchPrediction


class MatchContext(BaseModel):
    fixture: Fixture
    home_elo: float = 1500.0
    away_elo: float = 1500.0
    home_fifa_points: float = 0.0
    away_fifa_points: float = 0.0
    recent_results: list = []
    home_attack_strength: float = 1.0
    home_defense_vulnerability: float = 1.0
    away_attack_strength: float = 1.0
    away_defense_vulnerability: float = 1.0
    avg_home_goals: float = 1.5
    avg_away_goals: float = 1.2


class IPredictor(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def priority(self) -> int: ...

    @abstractmethod
    def predict(self, ctx: MatchContext) -> MatchPrediction: ...
