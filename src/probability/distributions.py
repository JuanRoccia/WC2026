import numpy as np
from scipy.stats import poisson
from src.config import settings
from src.models.prediction import OutcomeProbabilities


def elo_expectation(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def outcome_from_expectation(
    exp: float, rating_diff: float
) -> OutcomeProbabilities:
    draw_p = settings.elo_draw_base * np.exp(-abs(rating_diff) / 550.0) + settings.elo_draw_min
    home_win = exp * (1.0 - draw_p)
    away_win = (1.0 - exp) * (1.0 - draw_p)
    total = home_win + draw_p + away_win
    return OutcomeProbabilities(
        home_win=home_win / total,
        draw=draw_p / total,
        away_win=away_win / total,
    )


def poisson_prob(lam: float, k: int) -> float:
    return poisson.pmf(k, lam)


def dixon_coles_tau(
    h: int, a: int, lam_h: float, lam_a: float, rho: float = 0.0
) -> float:
    if rho == 0.0:
        return 1.0
    if h == 0 and a == 0:
        return 1.0 - lam_h * lam_a * rho
    elif h == 0 and a == 1:
        return 1.0 + lam_h * rho
    elif h == 1 and a == 0:
        return 1.0 + lam_a * rho
    elif h == 1 and a == 1:
        return 1.0 - rho
    return 1.0


def scoreline_matrix(
    lam_h: float, lam_a: float, max_goals: int = 8, rho: float = 0.0
) -> list[list[float]]:
    matrix = [[0.0] * (max_goals + 1) for _ in range(max_goals + 1)]
    total = 0.0
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            p = (
                poisson_prob(lam_h, i)
                * poisson_prob(lam_a, j)
                * dixon_coles_tau(i, j, lam_h, lam_a, rho)
            )
            matrix[i][j] = p
            total += p
    if total > 0:
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                matrix[i][j] /= total
    return matrix
