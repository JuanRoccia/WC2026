import numpy as np
from src.predictors.base import IPredictor, MatchContext
from src.predictors.goal_model import GoalModel
from src.models.prediction import MatchPrediction, OutcomeProbabilities, ScorelineDistribution
from src.probability import scoreline_matrix
from src.config import settings


class GoalPlusRecentContextModel(IPredictor):
    def __init__(self):
        self._goal_model = GoalModel()

    @property
    def name(self) -> str:
        return "Goles + Contexto"

    @property
    def priority(self) -> int:
        return 5

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        base = self._goal_model.predict(ctx)
        if base.is_degraded:
            return base

        fc = ctx.fixture.context
        lam_h = base.expected_home_goals
        lam_a = base.expected_away_goals

        if fc.home_unavailable_attack_impact > 0:
            lam_h *= max(0.82, 1.0 - fc.home_unavailable_attack_impact)
        if fc.away_unavailable_attack_impact > 0:
            lam_a *= max(0.82, 1.0 - fc.away_unavailable_attack_impact)
        if fc.home_unavailable_defense_impact > 0:
            lam_a *= max(0.86, 1.0 - fc.home_unavailable_defense_impact)
        if fc.away_unavailable_defense_impact > 0:
            lam_h *= max(0.86, 1.0 - fc.away_unavailable_defense_impact)
        if fc.home_unavailable_players > 0 and fc.home_unavailable_attack_impact == 0:
            lam_h *= max(0.86, 1.0 - fc.home_unavailable_players * 0.02)
        if fc.away_unavailable_players > 0 and fc.away_unavailable_attack_impact == 0:
            lam_a *= max(0.86, 1.0 - fc.away_unavailable_players * 0.02)

        matrix = scoreline_matrix(lam_h, lam_a, rho=settings.dixon_coles_rho)

        home_win_p = sum(matrix[i][j] for i in range(9) for j in range(9) if i > j)
        draw_p = sum(matrix[i][i] for i in range(9))
        away_win_p = sum(matrix[i][j] for i in range(9) for j in range(9) if i < j)

        outcome = OutcomeProbabilities(
            home_win=home_win_p, draw=draw_p, away_win=away_win_p,
        ).normalize()

        features = base.features_used + ["player_availability"]
        features_missing = []
        if fc.home_unavailable_players == 0 and fc.away_unavailable_players == 0:
            features_missing.append("player_availability_data")

        max_score = max(
            ((i, j) for i in range(9) for j in range(9)),
            key=lambda x: matrix[x[0]][x[1]],
        )

        return MatchPrediction(
            predictor_name=self.name,
            priority=self.priority,
            outcome=outcome,
            expected_home_goals=lam_h,
            expected_away_goals=lam_a,
            scoreline=ScorelineDistribution(matrix=matrix),
            most_likely_score=max_score,
            features_used=features,
            features_missing=features_missing,
            explanation=(
                f"{base.explanation} "
                f"Ajustado por disponibilidad: "
                f"{fc.home_unavailable_players} bajas local, "
                f"{fc.away_unavailable_players} bajas visita."
            ),
        )
