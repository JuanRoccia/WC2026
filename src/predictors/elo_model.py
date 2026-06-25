from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction
from src.probability import elo_expectation, outcome_from_expectation


class EloModel(IPredictor):
    @property
    def name(self) -> str:
        return "Rating Elo"

    @property
    def priority(self) -> int:
        return 2

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        if ctx.home_elo <= 0 or ctx.away_elo <= 0:
            return MatchPrediction(
                predictor_name=self.name,
                priority=self.priority,
                explanation="Faltan datos de rating Elo.",
                features_missing=["elo_rating"],
                is_degraded=True,
            )

        diff = ctx.home_elo - ctx.away_elo
        exp = elo_expectation(ctx.home_elo, ctx.away_elo)
        outcome = outcome_from_expectation(exp, diff)

        return MatchPrediction(
            predictor_name=self.name,
            priority=self.priority,
            outcome=outcome,
            features_used=["elo_rating"],
            explanation=(
                f"Basado en rating Elo. {ctx.fixture.home_team_name} "
                f"({ctx.home_elo:.0f}) vs "
                f"{ctx.fixture.away_team_name} ({ctx.away_elo:.0f}). "
                f"Diferencia: {diff:+.0f} pts Elo."
            ),
        )
