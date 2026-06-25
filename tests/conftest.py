import pytest
from src.models.fixture import Fixture, MatchResult, FixtureContext
from src.models.team import Team, Group
from src.models.prediction import OutcomeProbabilities
from src.predictors.base import MatchContext


@pytest.fixture
def basic_fixture() -> Fixture:
    return Fixture(
        id="group_A_1",
        group_name="A",
        home_team_id="mexico",
        away_team_id="south_africa",
        home_team_name="Mexico",
        away_team_name="South Africa",
    )


@pytest.fixture
def played_fixture() -> Fixture:
    return Fixture(
        id="group_A_2",
        group_name="A",
        home_team_id="mexico",
        away_team_id="south_korea",
        home_team_name="Mexico",
        away_team_name="South Korea",
        is_played=True,
        result=MatchResult(home_goals=2, away_goals=1),
    )


@pytest.fixture
def match_context(basic_fixture) -> MatchContext:
    return MatchContext(
        fixture=basic_fixture,
        home_elo=1800.0,
        away_elo=1700.0,
        home_fifa_points=1500.0,
        away_fifa_points=1400.0,
        home_attack_strength=1.2,
        home_defense_vulnerability=0.9,
        away_attack_strength=0.8,
        away_defense_vulnerability=1.1,
        avg_home_goals=1.5,
        avg_away_goals=1.2,
    )


@pytest.fixture
def uniform_outcome() -> OutcomeProbabilities:
    return OutcomeProbabilities(home_win=1/3, draw=1/3, away_win=1/3)
