import numpy as np
from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction, OutcomeProbabilities, ScorelineDistribution
from src.probability import scoreline_matrix
from src.config import settings


class GoalModel(IPredictor):
    @property
    def name(self) -> str:
        return "Modelo de goles"

    @property
    def priority(self) -> int:
        return 4

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        if ctx.home_attack_strength <= 0 or ctx.away_attack_strength <= 0:
            return MatchPrediction(
                predictor_name=self.name,
                priority=self.priority,
                explanation="Faltan datos históricos de goles para el modelo.",
                features_missing=["historical_goals"],
                is_degraded=True,
            )

        avg_h = ctx.avg_home_goals
        avg_a = ctx.avg_away_goals

        if not ctx.fixture.is_neutral:
            home_factor = settings.home_advantage
        else:
            home_factor = 1.0

        lam_h = avg_h * ctx.home_attack_strength * ctx.away_defense_vulnerability * home_factor
        lam_a = avg_a * ctx.away_attack_strength * ctx.home_defense_vulnerability

        matrix = scoreline_matrix(lam_h, lam_a, rho=settings.dixon_coles_rho)

        home_win_p = sum(matrix[i][j] for i in range(9) for j in range(9) if i > j)
        draw_p = sum(matrix[i][i] for i in range(9))
        away_win_p = sum(matrix[i][j] for i in range(9) for j in range(9) if i < j)

        outcome = OutcomeProbabilities(
            home_win=home_win_p,
            draw=draw_p,
            away_win=away_win_p,
        ).normalize()

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
            features_used=["attack_strength", "defense_vulnerability", "avg_goals"],
            explanation=(
                f"Modelo Poisson con correccion Dixon-Coles. "
                f"Goles esperados: {ctx.fixture.home_team_name} {lam_h:.2f}, "
                f"{ctx.fixture.away_team_name} {lam_a:.2f}. "
                f"Ataque local: {ctx.home_attack_strength:.2f}, "
                f"Defensa local: {ctx.home_defense_vulnerability:.2f}, "
                f"Ataque visita: {ctx.away_attack_strength:.2f}, "
                f"Defensa visita: {ctx.away_defense_vulnerability:.2f}."
            ),
        )
