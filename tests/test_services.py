import pytest
from src.services.data_service import DataService
from src.services.evaluation_service import EvaluationService
from src.models.prediction import OutcomeProbabilities
from src.models.fixture import Fixture
from src.data.persistence import load_results_json, build_results_entries
from src.config import settings


class TestDataService:
    def test_get_groups_summary(self):
        svc = DataService()
        groups = svc.get_groups_summary()
        assert len(groups) == 12
        assert all("name" in g and "teams" in g for g in groups)
        assert all(len(g["teams"]) == 4 for g in groups)

    def test_get_team_list(self):
        svc = DataService()
        teams = svc.get_team_list()
        assert len(teams) == 48
        assert all("id" in t and "name" in t and "group" in t for t in teams)

    def test_get_elo_rankings(self):
        svc = DataService()
        rankings = svc.get_elo_rankings()
        assert len(rankings) > 0
        assert all("team" in r and "rating" in r for r in rankings)
        for i in range(len(rankings) - 1):
            assert rankings[i]["rating"] >= rankings[i + 1]["rating"]

    def test_get_fifa_rankings(self):
        svc = DataService()
        rankings = svc.get_fifa_rankings()
        assert len(rankings) > 0
        assert all("team" in r and "points" in r and "rank" in r for r in rankings)


class TestEvaluationService:
    def test_evaluate_returns_evaluation(self):
        svc = EvaluationService()
        pred = OutcomeProbabilities(home_win=0.5, draw=0.3, away_win=0.2)
        eval_result = svc.evaluate(pred, 2, 1, "Test Predictor", "fix_1")
        assert eval_result.fixture_id == "fix_1"
        assert eval_result.predictor_name == "Test Predictor"
        assert eval_result.home_win_p == 0.5
        assert 0 <= eval_result.brier_score <= 2

    def test_evaluate_home_win_correct(self):
        svc = EvaluationService()
        pred = OutcomeProbabilities(home_win=0.8, draw=0.1, away_win=0.1)
        eval_result = svc.evaluate(pred, 3, 0, "Model", "fix_1")
        assert eval_result.top_pick_correct

    def test_evaluate_home_win_incorrect(self):
        svc = EvaluationService()
        pred = OutcomeProbabilities(home_win=0.8, draw=0.1, away_win=0.1)
        eval_result = svc.evaluate(pred, 0, 2, "Model", "fix_1")
        assert not eval_result.top_pick_correct

    def test_get_performance_empty(self):
        svc = EvaluationService()
        perf = svc.get_performance()
        assert perf == []

    def test_get_performance_after_evaluations(self):
        svc = EvaluationService()
        pred = OutcomeProbabilities(home_win=0.6, draw=0.2, away_win=0.2)
        svc.evaluate(pred, 1, 0, "Model A", "fix_1")
        svc.evaluate(pred, 0, 1, "Model A", "fix_2")
        perf = svc.get_performance()
        assert len(perf) == 1
        assert perf[0].predictor_name == "Model A"
        assert perf[0].sample_count == 2
        assert 0 <= perf[0].top_pick_accuracy <= 1

    def test_multiple_predictors(self):
        svc = EvaluationService()
        svc.evaluate(OutcomeProbabilities(home_win=0.6, draw=0.2, away_win=0.2), 1, 0, "A", "f1")
        svc.evaluate(OutcomeProbabilities(home_win=0.3, draw=0.4, away_win=0.3), 0, 0, "B", "f2")
        perf = svc.get_performance()
        assert len(perf) == 2
        names = [r.predictor_name for r in perf]
        assert "A" in names
        assert "B" in names


class TestPersistence:
    def test_load_results_json_returns_list(self):
        results = load_results_json()
        assert isinstance(results, list)

    def test_build_results_entries(self):
        from src.data.loader import load_all_data
        from src.services.prediction_service import PredictionService
        data = load_all_data()
        if data["fixtures"]:
            data["fixtures"][0].is_played = True
            data["fixtures"][0].result = type("R", (), {"home_goals": 1, "away_goals": 0})()
        entries = build_results_entries(type("PS", (), {"data": data})())
        assert isinstance(entries, list)
