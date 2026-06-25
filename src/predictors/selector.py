from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction, MatchPredictionResult
from src.probability import elo_expectation
from src.config import settings


class FinalPredictionSelector:
    def __init__(self, predictors: list[IPredictor]):
        self.predictors = sorted(predictors, key=lambda p: p.priority)

    def select(self, ctx: MatchContext, ladder: list[MatchPrediction]) -> MatchPredictionResult:
        result = MatchPredictionResult(
            fixture_id=ctx.fixture.id,
            ladder=ladder,
        )

        non_degraded = [p for p in ladder if not p.is_degraded]
        if not non_degraded:
            result.best_prediction = ladder[0]
            result.selected_predictor = ladder[0].predictor_name
            return result

        best = max(non_degraded, key=lambda p: p.priority)
        result.best_prediction = best
        result.selected_predictor = best.predictor_name

        # Calibration: if both Elo and FIFA agree against the selected model
        fifa_pred = next((p for p in ladder if p.predictor_name == "Ranking FIFA"), None)
        elo_pred = next((p for p in ladder if p.predictor_name == "Rating Elo"), None)
        goal_pred = next((p for p in ladder if p.predictor_name == "Modelo de goles"), None)

        if goal_pred and fifa_pred and elo_pred and not fifa_pred.is_degraded and not elo_pred.is_degraded:
            fifa_pick = fifa_pred.outcome.top_pick
            elo_pick = elo_pred.outcome.top_pick
            best_pick = best.outcome.top_pick

            if fifa_pick == elo_pick and fifa_pick != best_pick:
                w = settings.ranking_calibration_weight
                o = best.outcome
                best.outcome = best.outcome.__class__(
                    home_win=(1 - w) * o.home_win + w * fifa_pred.outcome.home_win,
                    draw=(1 - w) * o.draw + w * fifa_pred.outcome.draw,
                    away_win=(1 - w) * o.away_win + w * fifa_pred.outcome.away_win,
                ).normalize()

        return result
