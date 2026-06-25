from pydantic import BaseModel
from datetime import datetime


class PredictionEvaluation(BaseModel):
    id: str = ""
    fixture_id: str
    predictor_name: str
    home_win_p: float = 0.0
    draw_p: float = 0.0
    away_win_p: float = 0.0
    actual_home_goals: int = 0
    actual_away_goals: int = 0
    brier_score: float = 0.0
    rps: float = 0.0
    log_loss: float = 0.0
    top_pick_correct: bool = False
    evaluated_at: datetime = datetime.now()


class ModelPerformanceRow(BaseModel):
    predictor_name: str
    sample_count: int = 0
    avg_brier: float = 0.0
    avg_rps: float = 0.0
    avg_log_loss: float = 0.0
    top_pick_accuracy: float = 0.0
