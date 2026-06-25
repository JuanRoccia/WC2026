import itertools
import pandas as pd
from src.data.loader import load_all_data
from src.predictors.base import IPredictor, MatchContext
from src.predictors.null_model import NullModel
from src.predictors.fifa_ranking import FifaRankingModel
from src.predictors.elo_model import EloModel
from src.predictors.recent_form import RecentFormModel
from src.predictors.goal_model import GoalModel
from src.predictors.goal_plus_context import GoalPlusRecentContextModel
from src.predictors.selector import FinalPredictionSelector
from src.models.prediction import OutcomeProbabilities, MatchPredictionResult
from src.config import settings


class DirectPrediction:
    def __init__(self, outcome: OutcomeProbabilities, expected_home_goals: float, expected_away_goals: float):
        self.home_win = outcome.home_win
        self.draw = outcome.draw
        self.away_win = outcome.away_win
        self.top_pick = outcome.top_pick
        self.expected_home_goals = expected_home_goals
        self.expected_away_goals = expected_away_goals


class PredictionService:
    def __init__(self):
        self.data = load_all_data()
        self.predictors: list[IPredictor] = [
            NullModel(),
            FifaRankingModel(),
            EloModel(),
            RecentFormModel(),
            GoalModel(),
            GoalPlusRecentContextModel(),
        ]
        self.selector = FinalPredictionSelector(self.predictors)
        self._cache: dict[str, MatchPredictionResult] = {}
        self._direct_cache: dict[tuple[str, str], OutcomeProbabilities] = {}
        self._team_strengths: dict[str, tuple[float, float]] = {}
        self._recent_results: list = []
        self._league_avg_home = 1.5
        self._league_avg_away = 1.2
        self._build_team_strengths()

    def _cache_key(self, fixture_id: str) -> str:
        fixture = next((f for f in self.data["fixtures"] if f.id == fixture_id), None)
        if not fixture:
            return fixture_id
        return f"{fixture_id}:{fixture.is_played}:{fixture.result}"

    def predict_match(self, fixture_id: str) -> MatchPredictionResult | None:
        key = self._cache_key(fixture_id)
        if key in self._cache:
            return self._cache[key]

        fixture = next((f for f in self.data["fixtures"] if f.id == fixture_id), None)
        if not fixture:
            return None

        ctx = self._build_context(fixture)
        ladder = []
        for p in self.predictors:
            ladder.append(p.predict(ctx))

        result = self.selector.select(ctx, ladder)
        self._cache[key] = result
        return result

    def predict_all_fixtures(self) -> list[MatchPredictionResult]:
        return [
            self.predict_match(f.id)
            for f in self.data["fixtures"]
            if not f.is_played
        ]

    def predict_direct(self, home_id: str, away_id: str) -> DirectPrediction:
        key = (home_id, away_id)
        if key in self._direct_cache:
            return self._direct_cache[key]

        ctx = MatchContext(
            fixture=self.data["fixtures"][0].model_copy(update={
                "home_team_id": home_id,
                "away_team_id": away_id,
                "home_team_name": home_id.replace("_", " ").title(),
                "away_team_name": away_id.replace("_", " ").title(),
            }),
        )
        self._populate_team_context(ctx, home_id, away_id)
        ladder = [p.predict(ctx) for p in self.predictors]
        result = self.selector.select(ctx, ladder)
        bp = result.best_prediction
        if bp:
            dp = DirectPrediction(bp.outcome, bp.expected_home_goals, bp.expected_away_goals)
        else:
            dp = DirectPrediction(OutcomeProbabilities(), 0.0, 0.0)
        self._direct_cache[key] = dp
        return dp

    def precompute_group_fixtures(self):
        for f in self.data["fixtures"]:
            self.predict_direct(f.home_team_id, f.away_team_id)

    def precompute_all_matchups(self, team_ids: list[str]):
        for h, a in itertools.permutations(team_ids, 2):
            self.predict_direct(h, a)

    def invalidate_direct_cache(self):
        self._direct_cache.clear()
        self._cache.clear()

    def _build_team_strengths(self):
        df = self.data["historical"]
        recent = df[df["date"] >= "2022-01-01"].copy()
        if len(recent) == 0:
            return

        recent["home_id"] = recent["home_team"].str.lower().str.replace(" ", "_")
        recent["away_id"] = recent["away_team"].str.lower().str.replace(" ", "_")

        name_fix = {
            "congo_dr": "dr_congo",
            "curacao": "curaçao",
            "czechia": "czech_republic",
        }
        for wc, hist in name_fix.items():
            recent.loc[recent["home_id"] == hist, "home_id"] = wc
            recent.loc[recent["away_id"] == hist, "away_id"] = wc

        self._league_avg_home = recent["home_score"].mean()
        self._league_avg_away = recent["away_score"].mean()
        self._recent_results = recent.to_dict("records")

        team_ids = {t.id for g in self.data["groups"] for t in g.teams}
        league_avg = (self._league_avg_home + self._league_avg_away) / 2
        for team_id in team_ids:
            as_home = recent[recent["home_id"] == team_id]
            as_away = recent[recent["away_id"] == team_id]
            scored = pd.concat([as_home["home_score"], as_away["away_score"]])
            conceded = pd.concat([as_home["away_score"], as_away["home_score"]])
            if len(scored) == 0 or league_avg <= 0:
                self._team_strengths[team_id] = (1.0, 1.0)
            else:
                atk = scored.mean() / league_avg
                dfn = conceded.mean() / league_avg
                self._team_strengths[team_id] = (
                    max(settings.goal_strength_min, min(settings.goal_strength_max, atk)),
                    max(settings.goal_strength_min, min(settings.goal_strength_max, dfn)),
                )

    def _populate_team_context(self, ctx: MatchContext, home_id: str, away_id: str):
        elo_h = self.data["elo_ratings"].get(home_id)
        elo_a = self.data["elo_ratings"].get(away_id)
        fifa_h = self.data["fifa_ratings"].get(home_id)
        fifa_a = self.data["fifa_ratings"].get(away_id)
        if elo_h: ctx.home_elo = elo_h.value
        if elo_a: ctx.away_elo = elo_a.value
        if fifa_h: ctx.home_fifa_points = fifa_h.value
        if fifa_a: ctx.away_fifa_points = fifa_a.value

        ctx.avg_home_goals = self._league_avg_home
        ctx.avg_away_goals = self._league_avg_away
        ctx.recent_results = self._recent_results

        home_atk, home_def = self._team_strengths.get(home_id, (1.0, 1.0))
        away_atk, away_def = self._team_strengths.get(away_id, (1.0, 1.0))
        ctx.home_attack_strength = home_atk
        ctx.home_defense_vulnerability = home_def
        ctx.away_attack_strength = away_atk
        ctx.away_defense_vulnerability = away_def

    def _build_context(self, fixture) -> MatchContext:
        ctx = MatchContext(fixture=fixture)
        self._populate_team_context(ctx, fixture.home_team_id, fixture.away_team_id)
        return ctx
