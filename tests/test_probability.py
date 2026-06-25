import numpy as np
import pytest
from src.probability import (
    elo_expectation,
    outcome_from_expectation,
    poisson_prob,
    dixon_coles_tau,
    scoreline_matrix,
)
from src.probability.metrics import brier_score, rps_score, log_loss_score
from src.models.prediction import OutcomeProbabilities
from src.config import settings


class TestEloExpectation:
    def test_equal_ratings(self):
        assert elo_expectation(1500, 1500) == pytest.approx(0.5, abs=1e-10)

    def test_higher_rating_favored(self):
        exp = elo_expectation(2000, 1500)
        assert exp > 0.9
        assert exp < 1.0

    def test_lower_rating_underdog(self):
        exp = elo_expectation(1500, 2000)
        assert exp > 0.0
        assert exp < 0.1

    def test_symmetric(self):
        a, b = 1750, 1620
        assert elo_expectation(a, b) + elo_expectation(b, a) == pytest.approx(1.0, abs=1e-10)

    def test_extreme_ratings(self):
        exp = elo_expectation(3000, 1000)
        assert exp > 0.999


class TestOutcomeFromExpectation:
    def test_returns_outcome(self):
        outcome = outcome_from_expectation(0.6, 50)
        assert 0 < outcome.home_win < 1
        assert 0 < outcome.draw < 1
        assert 0 < outcome.away_win < 1
        assert outcome.home_win + outcome.draw + outcome.away_win == pytest.approx(1.0, abs=1e-6)

    def test_favored_team_higher(self):
        outcome = outcome_from_expectation(0.8, 100)
        assert outcome.home_win > outcome.away_win

    def test_underdog_lower(self):
        outcome = outcome_from_expectation(0.2, -100)
        assert outcome.away_win > outcome.home_win


class TestPoissonProb:
    def test_known_values(self):
        assert poisson_prob(1.0, 0) == pytest.approx(np.exp(-1), abs=1e-10)
        assert poisson_prob(1.0, 1) == pytest.approx(np.exp(-1), abs=1e-10)

    def test_zero_lambda(self):
        assert poisson_prob(0.0, 0) == pytest.approx(1.0, abs=1e-10)
        assert poisson_prob(0.0, 1) == pytest.approx(0.0, abs=1e-10)


class TestDixonColesTau:
    def test_rho_zero_always_one(self):
        assert dixon_coles_tau(0, 0, 1.0, 1.0, 0.0) == 1.0
        assert dixon_coles_tau(2, 3, 1.0, 1.0, 0.0) == 1.0

    def test_rho_nonzero_00(self):
        tau = dixon_coles_tau(0, 0, 1.0, 1.0, 0.1)
        assert tau == pytest.approx(1.0 - 1.0 * 1.0 * 0.1, abs=1e-10)

    def test_rho_nonzero_01(self):
        tau = dixon_coles_tau(0, 1, 1.0, 1.0, 0.1)
        assert tau == pytest.approx(1.0 + 1.0 * 0.1, abs=1e-10)

    def test_rho_nonzero_10(self):
        tau = dixon_coles_tau(1, 0, 1.0, 1.0, 0.1)
        assert tau == pytest.approx(1.0 + 1.0 * 0.1, abs=1e-10)

    def test_rho_nonzero_11(self):
        tau = dixon_coles_tau(1, 1, 1.0, 1.0, 0.1)
        assert tau == pytest.approx(1.0 - 0.1, abs=1e-10)

    def test_high_scores_always_one(self):
        assert dixon_coles_tau(4, 2, 1.0, 1.0, 0.1) == 1.0
        assert dixon_coles_tau(0, 3, 1.0, 1.0, 0.1) == 1.0


class TestScorelineMatrix:
    def test_dimensions(self):
        matrix = scoreline_matrix(1.0, 1.0)
        assert len(matrix) == 9
        assert all(len(row) == 9 for row in matrix)

    def test_normalized(self):
        matrix = scoreline_matrix(1.0, 1.0)
        total = sum(matrix[i][j] for i in range(9) for j in range(9))
        assert total == pytest.approx(1.0, abs=1e-6)

    def test_home_favored(self):
        matrix = scoreline_matrix(2.0, 0.5)
        home = sum(matrix[i][j] for i in range(9) for j in range(9) if i > j)
        away = sum(matrix[i][j] for i in range(9) for j in range(9) if i < j)
        assert home > away

    def test_symmetric_when_equal(self):
        matrix = scoreline_matrix(1.0, 1.0)
        home = sum(matrix[i][j] for i in range(9) for j in range(9) if i > j)
        away = sum(matrix[i][j] for i in range(9) for j in range(9) if i < j)
        assert home == pytest.approx(away, abs=0.02)

    def test_all_non_negative(self):
        matrix = scoreline_matrix(1.5, 1.2)
        assert all(matrix[i][j] >= 0 for i in range(9) for j in range(9))


class TestBrierScore:
    def test_perfect_prediction(self):
        pred = OutcomeProbabilities(home_win=1.0, draw=0.0, away_win=0.0)
        assert brier_score(pred, True, False, False) == pytest.approx(0.0, abs=1e-10)

    def test_worst_prediction(self):
        pred = OutcomeProbabilities(home_win=1.0, draw=0.0, away_win=0.0)
        assert brier_score(pred, False, False, True) == pytest.approx(2.0, abs=1e-10)

    def test_uniform_prediction(self):
        pred = OutcomeProbabilities(home_win=1/3, draw=1/3, away_win=1/3)
        score = brier_score(pred, True, False, False)
        expected = (1/3 - 1)**2 + (1/3 - 0)**2 + (1/3 - 0)**2
        assert score == pytest.approx(expected, abs=1e-10)


class TestRpsScore:
    def test_perfect_prediction(self):
        pred = OutcomeProbabilities(home_win=1.0, draw=0.0, away_win=0.0)
        assert rps_score(pred, True, False, False) == pytest.approx(0.0, abs=1e-10)

    def test_range(self):
        pred = OutcomeProbabilities(home_win=1/3, draw=1/3, away_win=1/3)
        score = rps_score(pred, True, False, False)
        assert 0 <= score <= 0.5


class TestLogLossScore:
    def test_certain_prediction(self):
        pred = OutcomeProbabilities(home_win=1.0, draw=0.0, away_win=0.0)
        assert log_loss_score(pred, True, False, False) == pytest.approx(0.0, abs=1e-10)

    def test_uniform_prediction(self):
        pred = OutcomeProbabilities(home_win=1/3, draw=1/3, away_win=1/3)
        score = log_loss_score(pred, True, False, False)
        assert score == pytest.approx(-np.log(1/3), abs=1e-10)

    def test_no_log_of_zero(self):
        pred = OutcomeProbabilities(home_win=0.0, draw=0.0, away_win=1.0)
        score = log_loss_score(pred, True, False, False)
        assert np.isfinite(score)

