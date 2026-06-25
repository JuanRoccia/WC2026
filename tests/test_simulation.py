import pytest
from src.simulation.group_table import GroupTableCalculator
from src.simulation.monte_carlo import MonteCarloSimulator
from src.simulation.annex_c import get_third_place_assignments
from src.models.fixture import Fixture, MatchResult
from src.models.tournament import KnockoutStage, GroupTableEntry


class TestGroupTableCalculator:
    def test_empty_fixtures(self):
        entries = GroupTableCalculator.calculate([])
        assert entries == []

    def test_single_match(self):
        fixtures = [
            Fixture(
                id="g1_m1", group_name="A",
                home_team_id="a", away_team_id="b",
                home_team_name="A", away_team_name="B",
                is_played=True,
                result=MatchResult(home_goals=2, away_goals=1),
            ),
        ]
        entries = GroupTableCalculator.calculate(fixtures)
        assert len(entries) == 2
        home = next(e for e in entries if e.team_id == "a")
        away = next(e for e in entries if e.team_id == "b")
        assert home.played == 1 and home.won == 1 and home.points == 3
        assert away.played == 1 and away.lost == 1 and away.points == 0

    def test_draw(self):
        fixtures = [
            Fixture(
                id="g1_m1", group_name="A",
                home_team_id="a", away_team_id="b",
                home_team_name="A", away_team_name="B",
                is_played=True,
                result=MatchResult(home_goals=1, away_goals=1),
            ),
        ]
        entries = GroupTableCalculator.calculate(fixtures)
        home = next(e for e in entries if e.team_id == "a")
        away = next(e for e in entries if e.team_id == "b")
        assert home.drawn == 1 and home.points == 1
        assert away.drawn == 1 and away.points == 1

    def test_unplayed_matches_ignored(self):
        fixtures = [
            Fixture(
                id="g1_m1", group_name="A",
                home_team_id="a", away_team_id="b",
                home_team_name="A", away_team_name="B",
                is_played=False,
            ),
        ]
        entries = GroupTableCalculator.calculate(fixtures)
        assert len(entries) == 2
        for e in entries:
            assert e.played == 0

    def test_sorting_by_points(self):
        fixtures = [
            Fixture(id="g1", group_name="A", home_team_id="a", away_team_id="b",
                    home_team_name="A", away_team_name="B",
                    is_played=True, result=MatchResult(home_goals=3, away_goals=0)),
            Fixture(id="g2", group_name="A", home_team_id="a", away_team_id="c",
                    home_team_name="A", away_team_name="C",
                    is_played=True, result=MatchResult(home_goals=1, away_goals=1)),
            Fixture(id="g3", group_name="A", home_team_id="b", away_team_id="c",
                    home_team_name="B", away_team_name="C",
                    is_played=True, result=MatchResult(home_goals=0, away_goals=2)),
        ]
        entries = GroupTableCalculator.calculate(fixtures)
        assert len(entries) == 3
        assert entries[0].team_id == "a"
        assert entries[1].team_id == "c"
        assert entries[2].team_id == "b"

    def test_resolve_tiebreaker_same_points(self):
        a = GroupTableEntry(team_id="a", points=4, goals_for=5, goals_against=3)
        b = GroupTableEntry(team_id="b", points=4, goals_for=4, goals_against=4)
        result = GroupTableCalculator.resolve_tiebreaker(a, b, {})
        assert result == -1

    def test_resolve_tiebreaker_different_points(self):
        a = GroupTableEntry(team_id="a", points=6)
        b = GroupTableEntry(team_id="b", points=3)
        result = GroupTableCalculator.resolve_tiebreaker(a, b, {})
        assert result == -1

    def test_resolve_tiebreaker_h2h(self):
        a = GroupTableEntry(team_id="a", points=4, goals_for=3, goals_against=3)
        b = GroupTableEntry(team_id="b", points=4, goals_for=3, goals_against=3)
        h2h = {"a": 3, "b": 1}
        result = GroupTableCalculator.resolve_tiebreaker(a, b, h2h)
        assert result == -1

    def test_resolve_tiebreaker_complete_tie(self):
        a = GroupTableEntry(team_id="a", points=4, goals_for=3, goals_against=3)
        b = GroupTableEntry(team_id="b", points=4, goals_for=3, goals_against=3)
        result = GroupTableCalculator.resolve_tiebreaker(a, b, {})
        assert result == 0


class TestMonteCarloSimulator:
    def test_next_stage_progression(self):
        sim = MonteCarloSimulator(lambda h, a: None, [])
        assert sim._next_stage(KnockoutStage.ROUND_OF_32) == KnockoutStage.ROUND_OF_16
        assert sim._next_stage(KnockoutStage.ROUND_OF_16) == KnockoutStage.QUARTERFINALS
        assert sim._next_stage(KnockoutStage.QUARTERFINALS) == KnockoutStage.SEMIFINALS
        assert sim._next_stage(KnockoutStage.SEMIFINALS) == KnockoutStage.FINAL
        assert sim._next_stage(KnockoutStage.FINAL) == KnockoutStage.FINAL

    def test_build_r32_matches_all_third_advance(self):
        sim = MonteCarloSimulator(lambda h, a: None, [])
        gw = {chr(65+i): f"team_{chr(65+i)}" for i in range(12)}
        gr = {chr(65+i): f"runner_{chr(65+i)}" for i in range(12)}
        atm = {chr(65+i): f"third_{chr(65+i)}" for i in range(12)}
        matches = sim._build_r32_matches(gw, gr, atm)
        assert len(matches) == 16

    def test_build_r32_matches_no_third_advancing(self):
        sim = MonteCarloSimulator(lambda h, a: None, [])
        gw = {chr(65+i): f"team_{chr(65+i)}" for i in range(12)}
        gr = {chr(65+i): f"runner_{chr(65+i)}" for i in range(12)}
        atm = {}
        matches = sim._build_r32_matches(gw, gr, atm)
        assert len(matches) == 16
        for i, m in matches:
            pass

    def test_play_ko_match_home_wins(self):
        def pred_fn(h, a):
            class FakePred:
                expected_home_goals = 3.0
                expected_away_goals = 0.5
            return FakePred()
        sim = MonteCarloSimulator(pred_fn, [])
        sim.rng = __import__("numpy").random.default_rng(42)
        winner = sim._play_ko_match("team_a", "team_b")
        assert winner == "team_a"

    def test_play_ko_match_none_returns_other(self):
        sim = MonteCarloSimulator(lambda h, a: None, [])
        assert sim._play_ko_match(None, "team_b") == "team_b"
        assert sim._play_ko_match("team_a", None) == "team_a"
        assert sim._play_ko_match(None, None) is None

    def test_r32_has_16_matches(self):
        sim = MonteCarloSimulator(lambda h, a: None, [])
        gw = {chr(65+i): "w"+chr(65+i) for i in range(12)}
        gr = {chr(65+i): "r"+chr(65+i) for i in range(12)}
        atm = {chr(65+i): "t"+chr(65+i) for i in range(12)}
        matches = sim._build_r32_matches(gw, gr, atm)
        assert len(matches) == 16


class TestAnnexC:
    def test_lookup_all_groups(self):
        advancing = list("ABCDEFGH")
        assignments = get_third_place_assignments(advancing)
        assert len(assignments) == 8

    def test_lookup_subset(self):
        advancing = list("CDEFGHIJ")
        assignments = get_third_place_assignments(advancing)
        assert len(assignments) == 8

    def test_lookup_unknown_combination(self):
        assignments = get_third_place_assignments(["A", "B"])
        assert assignments == {}

    def test_all_rows_unique(self):
        from src.simulation.annex_c import ANNEX_C_ROWS, ANNEX_C_LOOKUP
        assert len(ANNEX_C_ROWS) == 495
        assert len(ANNEX_C_LOOKUP) == 495
        sorted_sets = {"".join(sorted(r)) for r in ANNEX_C_ROWS}
        assert len(sorted_sets) == 495

    def test_each_row_has_8_distinct_letters(self):
        from src.simulation.annex_c import ANNEX_C_ROWS
        for row in ANNEX_C_ROWS:
            assert len(row) == 8
            assert len(set(row)) == 8

    def test_third_always_plays_winner(self):
        from src.simulation.annex_c import ANNEX_C_ROWS, ANNEX_C_WINNERS
        for row in ANNEX_C_ROWS:
            for i, ch in enumerate(row):
                assert ch != ANNEX_C_WINNERS[i], f"Self-match at {ANNEX_C_WINNERS[i]} vs 3{ch}"
