import numpy as np
from src.predictors.base import IPredictor, MatchContext
from src.models.prediction import MatchPrediction
from src.probability import elo_expectation, outcome_from_expectation
from src.config import settings


class RecentFormModel(IPredictor):
    @property
    def name(self) -> str:
        return "Forma reciente"

    @property
    def priority(self) -> int:
        return 3

    def predict(self, ctx: MatchContext) -> MatchPrediction:
        if ctx.home_elo <= 0 or ctx.away_elo <= 0:
            return MatchPrediction(
                predictor_name=self.name,
                priority=self.priority,
                explanation="Faltan ratings Elo para calcular forma reciente.",
                features_missing=["elo_rating"],
                is_degraded=True,
            )

        home_delta = self._form_delta(ctx.recent_results, ctx.fixture.home_team_id, ctx.home_elo)
        away_delta = self._form_delta(ctx.recent_results, ctx.fixture.away_team_id, ctx.away_elo)

        adj_home_elo = ctx.home_elo + home_delta
        adj_away_elo = ctx.away_elo + away_delta
        diff = adj_home_elo - adj_away_elo
        exp = elo_expectation(adj_home_elo, adj_away_elo)
        outcome = outcome_from_expectation(exp, diff)

        return MatchPrediction(
            predictor_name=self.name,
            priority=self.priority,
            outcome=outcome,
            features_used=["elo_rating", "recent_results"],
            explanation=(
                f"Forma reciente ajustada. Elo ajustado: "
                f"{ctx.fixture.home_team_name} {adj_home_elo:.0f} "
                f"(delta: {home_delta:+.0f}), "
                f"{ctx.fixture.away_team_name} {adj_away_elo:.0f} "
                f"(delta: {away_delta:+.0f})."
            ),
        )

    def _form_delta(self, results: list, team_id: str, base_elo: float) -> float:
        team_results = [r for r in results if r.get("home_id") == team_id or r.get("away_id") == team_id]
        if not team_results:
            return 0.0

        delta = 0.0
        total_weight = 0.0
        for i, r in enumerate(team_results[-settings.recent_result_count:]):
            weight = settings.form_recent_weight ** i
            is_home = r.get("home_id") == team_id
            gf = r.get("home_score") if is_home else r.get("away_score")
            ga = r.get("away_score") if is_home else r.get("home_score")
            if gf is None or ga is None or np.isnan(gf) or np.isnan(ga):
                continue
            gd = gf - ga
            if gf > ga:
                points = 3
            elif gf == ga:
                points = 1
            else:
                points = 0

            match_delta = weight * ((points - 0.2) * 18 + np.clip(gd, -3, 3) * 8)
            delta += match_delta
            total_weight += weight

        if total_weight > 0:
            delta /= total_weight

        return float(np.clip(delta, -100, 100))
