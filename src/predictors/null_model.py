from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction, OutcomeProbabilities


class NullModel(IPredictor):
    @property
    def name(self) -> str:
        return "Modelo base"

    @property
    def priority(self) -> int:
        return 0

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        return MatchPrediction(
            predictor_name=self.name,
            priority=self.priority,
            outcome=OutcomeProbabilities(
                home_win=1 / 3, draw=1 / 3, away_win=1 / 3
            ),
            explanation="Modelo base: probabilidad uniforme del 33% para cada resultado.",
            is_degraded=False,
        )
