from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction
from src.probability import elo_expectation, outcome_from_expectation


class FifaRankingModel(IPredictor):
    @property
    def name(self) -> str:
        return "Ranking FIFA"

    @property
    def priority(self) -> int:
        return 1

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        if ctx.home_fifa_points <= 0 or ctx.away_fifa_points <= 0:
            return MatchPrediction(
                predictor_name=self.name,
                priority=self.priority,
                explanation="Faltan datos de ranking FIFA.",
                features_missing=["fifa_points"],
                is_degraded=True,
            )

        diff = ctx.home_fifa_points - ctx.away_fifa_points
        exp = elo_expectation(ctx.home_fifa_points, ctx.away_fifa_points)
        outcome = outcome_from_expectation(exp, diff)

        return MatchPrediction(
            predictor_name=self.name,
            priority=self.priority,
            outcome=outcome,
            features_used=["fifa_points"],
            explanation=(
                f"Basado en ranking FIFA. {ctx.fixture.home_team_name} "
                f"({ctx.home_fifa_points:.0f} pts) vs "
                f"{ctx.fixture.away_team_name} ({ctx.away_fifa_points:.0f} pts). "
                f"Diferencia: {diff:+.0f} pts."
            ),
        )
