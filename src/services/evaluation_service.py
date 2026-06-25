from src.models.prediction import OutcomeProbabilities
from src.models.evaluation import PredictionEvaluation, ModelPerformanceRow
from src.probability import brier_score, rps_score, log_loss_score


class EvaluationService:
    def __init__(self):
        self.evaluations: list[PredictionEvaluation] = []

    def evaluate(
        self,
        pred: OutcomeProbabilities,
        actual_home_goals: int,
        actual_away_goals: int,
        predictor_name: str = "",
        fixture_id: str = "",
    ) -> PredictionEvaluation:
        actual_home = actual_home_goals > actual_away_goals
        actual_draw = actual_home_goals == actual_away_goals
        actual_away = actual_home_goals < actual_away_goals

        evaluation = PredictionEvaluation(
            fixture_id=fixture_id,
            predictor_name=predictor_name,
            home_win_p=pred.home_win,
            draw_p=pred.draw,
            away_win_p=pred.away_win,
            actual_home_goals=actual_home_goals,
            actual_away_goals=actual_away_goals,
            brier_score=brier_score(pred, actual_home, actual_draw, actual_away),
            rps=rps_score(pred, actual_home, actual_draw, actual_away),
            log_loss=log_loss_score(pred, actual_home, actual_draw, actual_away),
            top_pick_correct=pred.top_pick == ("home" if actual_home else "draw" if actual_draw else "away"),
        )
        self.evaluations.append(evaluation)
        return evaluation

    def get_performance(self) -> list[ModelPerformanceRow]:
        grouped: dict[str, list[PredictionEvaluation]] = {}
        for e in self.evaluations:
            grouped.setdefault(e.predictor_name, []).append(e)

        rows = []
        for name, evals in grouped.items():
            n = len(evals)
            rows.append(ModelPerformanceRow(
                predictor_name=name,
                sample_count=n,
                avg_brier=sum(e.brier_score for e in evals) / n,
                avg_rps=sum(e.rps for e in evals) / n,
                avg_log_loss=sum(e.log_loss for e in evals) / n,
                top_pick_accuracy=sum(1 for e in evals if e.top_pick_correct) / n,
            ))
        return sorted(rows, key=lambda r: r.avg_rps)
