from datetime import datetime
from pydantic import BaseModel
import numpy as np


class OutcomeProbabilities(BaseModel):
    home_win: float = 0.0
    draw: float = 0.0
    away_win: float = 0.0

    def normalize(self) -> "OutcomeProbabilities":
        total = self.home_win + self.draw + self.away_win
        if total > 0:
            return OutcomeProbabilities(
                home_win=self.home_win / total,
                draw=self.draw / total,
                away_win=self.away_win / total,
            )
        return OutcomeProbabilities(home_win=1 / 3, draw=1 / 3, away_win=1 / 3)

    @property
    def top_pick(self) -> str:
        max_val = max(self.home_win, self.draw, self.away_win)
        if self.home_win == max_val:
            return "home"
        elif self.draw == max_val:
            return "draw"
        return "away"

    @property
    def as_array(self) -> np.ndarray:
        return np.array([self.home_win, self.draw, self.away_win])


class ScorelineDistribution(BaseModel):
    matrix: list[list[float]] | None = None

    def most_likely(self) -> tuple[int, int]:
        if not self.matrix:
            return (0, 0)
        flat = [(i, j, self.matrix[i][j]) for i in range(9) for j in range(9)]
        best = max(flat, key=lambda x: x[2])
        return (best[0], best[1])


class MatchPrediction(BaseModel):
    predictor_name: str
    priority: int
    outcome: OutcomeProbabilities = OutcomeProbabilities()
    expected_home_goals: float = 0.0
    expected_away_goals: float = 0.0
    scoreline: ScorelineDistribution = ScorelineDistribution()
    most_likely_score: tuple[int, int] = (0, 0)
    explanation: str = ""
    features_used: list[str] = []
    features_missing: list[str] = []
    is_degraded: bool = False


class MatchPredictionResult(BaseModel):
    fixture_id: str
    ladder: list[MatchPrediction] = []
    best_prediction: MatchPrediction | None = None
    selected_predictor: str = ""
    generated_at: datetime = datetime.now()


class PredictionSnapshot(BaseModel):
    id: str = ""
    fixture_id: str
    predictor_name: str
    home_goals: float = 0.0
    away_goals: float = 0.0
    home_win_p: float = 0.0
    draw_p: float = 0.0
    away_win_p: float = 0.0
    actual_home_goals: int | None = None
    actual_away_goals: int | None = None
    evaluated: bool = False
    created_at: datetime = datetime.now()
    snapshot_type: str = "match"
