import pytest
from src.predictors.null_model import NullModel
from src.predictors.fifa_ranking import FifaRankingModel
from src.predictors.elo_model import EloModel
from src.predictors.recent_form import RecentFormModel
from src.predictors.goal_model import GoalModel
from src.predictors.goal_plus_context import GoalPlusRecentContextModel
from src.predictors.selector import FinalPredictionSelector
from src.predictors.base import MatchContext
from src.models.fixture import Fixture, FixtureContext
from src.models.prediction import OutcomeProbabilities, MatchPrediction


@pytest.fixture
def ctx_with_data():
    return MatchContext(
        fixture=Fixture(
            id="test", group_name="X",
            home_team_id="team_a", away_team_id="team_b",
            home_team_name="Team A", away_team_name="Team B",
            context=FixtureContext(home_unavailable_players=2, away_unavailable_players=1),
        ),
        home_elo=1800.0, away_elo=1700.0,
        home_fifa_points=1600.0, away_fifa_points=1400.0,
        home_attack_strength=1.2, home_defense_vulnerability=0.9,
        away_attack_strength=0.8, away_defense_vulnerability=1.1,
        avg_home_goals=1.5, avg_away_goals=1.2,
        recent_results=[
            {"home_id": "team_a", "away_id": "team_c", "home_score": 2, "away_score": 0},
            {"home_id": "team_d", "away_id": "team_a", "home_score": 1, "away_score": 1},
        ],
    )


@pytest.fixture
def ctx_missing_data():
    return MatchContext(
        fixture=Fixture(id="test", group_name="X", home_team_id="team_a", away_team_id="team_b"),
        home_elo=0.0, away_elo=0.0,
        home_fifa_points=0.0, away_fifa_points=0.0,
        home_attack_strength=0.0, away_attack_strength=0.0,
        home_defense_vulnerability=0.0, away_defense_vulnerability=0.0,
    )


class TestNullModel:
    def test_name(self):
        assert NullModel().name == "Modelo base"

    def test_priority(self):
        assert NullModel().priority == 0

    def test_uniform_prediction(self, ctx_with_data):
        pred = NullModel().predict(ctx_with_data)
        assert pred.outcome.home_win == pytest.approx(1/3, abs=1e-6)
        assert pred.outcome.draw == pytest.approx(1/3, abs=1e-6)
        assert pred.outcome.away_win == pytest.approx(1/3, abs=1e-6)
        assert not pred.is_degraded


class TestFifaRankingModel:
    def test_name(self):
        assert FifaRankingModel().name == "Ranking FIFA"

    def test_priority(self):
        assert FifaRankingModel().priority == 1

    def test_prediction_with_data(self, ctx_with_data):
        pred = FifaRankingModel().predict(ctx_with_data)
        assert pred.outcome.home_win > pred.outcome.away_win
        assert not pred.is_degraded

    def test_degraded_when_missing(self, ctx_missing_data):
        pred = FifaRankingModel().predict(ctx_missing_data)
        assert pred.is_degraded
        assert "fifa_points" in pred.features_missing

    def test_explanation_mentions_points(self, ctx_with_data):
        pred = FifaRankingModel().predict(ctx_with_data)
        assert "pts" in pred.explanation
        assert "1600" in pred.explanation or "1400" in pred.explanation


class TestEloModel:
    def test_name(self):
        assert EloModel().name == "Rating Elo"

    def test_priority(self):
        assert EloModel().priority == 2

    def test_prediction_with_data(self, ctx_with_data):
        pred = EloModel().predict(ctx_with_data)
        assert pred.outcome.home_win > pred.outcome.away_win
        assert not pred.is_degraded

    def test_degraded_when_missing(self, ctx_missing_data):
        pred = EloModel().predict(ctx_missing_data)
        assert pred.is_degraded
        assert "elo_rating" in pred.features_missing

    def test_explanation_mentions_elo(self, ctx_with_data):
        pred = EloModel().predict(ctx_with_data)
        assert "Elo" in pred.explanation


class TestRecentFormModel:
    def test_name(self):
        assert RecentFormModel().name == "Forma reciente"

    def test_priority(self):
        assert RecentFormModel().priority == 3

    def test_prediction_with_data(self, ctx_with_data):
        pred = RecentFormModel().predict(ctx_with_data)
        assert not pred.is_degraded

    def test_degraded_when_missing_elo(self, ctx_missing_data):
        pred = RecentFormModel().predict(ctx_missing_data)
        assert pred.is_degraded

    def test_form_delta(self, ctx_with_data):
        model = RecentFormModel()
        delta = model._form_delta(ctx_with_data.recent_results, "team_a", 1800.0)
        assert isinstance(delta, float)

    def test_empty_results_returns_zero(self, ctx_with_data):
        model = RecentFormModel()
        delta = model._form_delta([], "team_a", 1800.0)
        assert delta == 0.0


class TestGoalModel:
    def test_name(self):
        assert GoalModel().name == "Modelo de goles"

    def test_priority(self):
        assert GoalModel().priority == 4

    def test_prediction_with_data(self, ctx_with_data):
        pred = GoalModel().predict(ctx_with_data)
        assert not pred.is_degraded
        assert pred.expected_home_goals > 0
        assert pred.expected_away_goals > 0

    def test_degraded_when_missing(self, ctx_missing_data):
        pred = GoalModel().predict(ctx_missing_data)
        assert pred.is_degraded
        assert "historical_goals" in pred.features_missing

    def test_outcome_sums_to_one(self, ctx_with_data):
        pred = GoalModel().predict(ctx_with_data)
        total = pred.outcome.home_win + pred.outcome.draw + pred.outcome.away_win
        assert total == pytest.approx(1.0, abs=1e-6)

    def test_most_likely_score_is_tuple(self, ctx_with_data):
        pred = GoalModel().predict(ctx_with_data)
        assert isinstance(pred.most_likely_score, tuple)
        assert len(pred.most_likely_score) == 2

    def test_explanation(self, ctx_with_data):
        pred = GoalModel().predict(ctx_with_data)
        assert "Poisson" in pred.explanation


class TestGoalPlusRecentContextModel:
    def test_name(self):
        assert GoalPlusRecentContextModel().name == "Goles + Contexto"

    def test_priority(self):
        assert GoalPlusRecentContextModel().priority == 5

    def test_prediction_with_data(self, ctx_with_data):
        pred = GoalPlusRecentContextModel().predict(ctx_with_data)
        assert not pred.is_degraded
        assert pred.expected_home_goals > 0

    def test_degraded_when_base_degraded(self, ctx_missing_data):
        pred = GoalPlusRecentContextModel().predict(ctx_missing_data)
        assert pred.is_degraded

    def test_context_adjusts_goals(self, ctx_with_data):
        ctx_with_data.fixture.context = FixtureContext(
            home_unavailable_attack_impact=0.3,
            away_unavailable_defense_impact=0.2,
        )
        pred = GoalPlusRecentContextModel().predict(ctx_with_data)
        assert isinstance(pred.expected_home_goals, float)

    def test_outcome_sums_to_one(self, ctx_with_data):
        pred = GoalPlusRecentContextModel().predict(ctx_with_data)
        total = pred.outcome.home_win + pred.outcome.draw + pred.outcome.away_win
        assert total == pytest.approx(1.0, abs=1e-6)


class TestFinalPredictionSelector:
    def test_select_best_non_degraded(self, ctx_with_data):
        null = NullModel()
        elo = EloModel()
        selector = FinalPredictionSelector([null, elo])
        ladder = [null.predict(ctx_with_data), elo.predict(ctx_with_data)]
        result = selector.select(ctx_with_data, ladder)
        assert result.selected_predictor == elo.name

    def test_falls_back_to_null_when_all_degraded(self, ctx_missing_data):
        null = NullModel()
        elo = EloModel()
        selector = FinalPredictionSelector([null, elo])
        ladder = [null.predict(ctx_missing_data), elo.predict(ctx_missing_data)]
        result = selector.select(ctx_missing_data, ladder)
        assert result.best_prediction is not None

    def test_selected_predictor_in_ladder(self, ctx_with_data):
        null = NullModel()
        elo = EloModel()
        selector = FinalPredictionSelector([null, elo])
        ladder = [null.predict(ctx_with_data), elo.predict(ctx_with_data)]
        result = selector.select(ctx_with_data, ladder)
        assert any(p.predictor_name == result.selected_predictor for p in result.ladder)


class TestOutcomeProbabilities:
    def test_normalize(self):
        o = OutcomeProbabilities(home_win=2.0, draw=1.0, away_win=1.0)
        n = o.normalize()
        assert n.home_win == pytest.approx(0.5, abs=1e-6)
        assert n.draw == pytest.approx(0.25, abs=1e-6)
        assert n.away_win == pytest.approx(0.25, abs=1e-6)

    def test_normalize_zero(self):
        o = OutcomeProbabilities(home_win=0.0, draw=0.0, away_win=0.0)
        n = o.normalize()
        assert n.home_win == pytest.approx(1/3, abs=1e-6)

    def test_top_pick_home(self):
        o = OutcomeProbabilities(home_win=0.5, draw=0.3, away_win=0.2)
        assert o.top_pick == "home"

    def test_top_pick_draw(self):
        o = OutcomeProbabilities(home_win=0.3, draw=0.5, away_win=0.2)
        assert o.top_pick == "draw"

    def test_top_pick_away(self):
        o = OutcomeProbabilities(home_win=0.2, draw=0.3, away_win=0.5)
        assert o.top_pick == "away"

    def test_as_array(self):
        o = OutcomeProbabilities(home_win=0.5, draw=0.3, away_win=0.2)
        import numpy as np
        arr = o.as_array
        assert isinstance(arr, np.ndarray)
        assert arr[0] == 0.5
        assert arr[1] == 0.3
        assert arr[2] == 0.2
