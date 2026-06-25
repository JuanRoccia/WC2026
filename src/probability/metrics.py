import numpy as np
from src.models.prediction import OutcomeProbabilities


def brier_score(pred: OutcomeProbabilities, actual_home: bool, actual_draw: bool, actual_away: bool) -> float:
    actual = np.array([float(actual_home), float(actual_draw), float(actual_away)])
    return float(np.sum((pred.as_array - actual) ** 2))


def rps_score(pred: OutcomeProbabilities, actual_home: bool, actual_draw: bool, actual_away: bool) -> float:
    actual = np.array([float(actual_home), float(actual_draw), float(actual_away)])
    pred_cumsum = np.cumsum(pred.as_array)
    actual_cumsum = np.cumsum(actual)
    return float(np.sum((pred_cumsum[:2] - actual_cumsum[:2]) ** 2) / 2.0)


def log_loss_score(pred: OutcomeProbabilities, actual_home: bool, actual_draw: bool, actual_away: bool) -> float:
    if actual_home:
        p = pred.home_win
    elif actual_draw:
        p = pred.draw
    else:
        p = pred.away_win
    p = max(p, 1e-15)
    return -np.log(p)
