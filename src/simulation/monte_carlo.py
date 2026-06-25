import numpy as np
from itertools import permutations
from collections import defaultdict
from src.config import settings
from src.models.fixture import Fixture
from src.models.prediction import OutcomeProbabilities
from src.models.tournament import (
    TournamentProjection, TeamTournamentProbability, KnockoutStage,
)
from src.simulation.annex_c import get_third_place_assignments


class MonteCarloSimulator:
    def __init__(self, predict_fn, team_ids: list[str] | None = None):
        self.predict_fn = predict_fn
        self.rng = np.random.default_rng(settings.simulation_seed)
        self._probs_cache: dict[tuple[str, str], OutcomeProbabilities] = {}
        if team_ids:
            self._precompute(team_ids)

    def _precompute(self, team_ids: list[str]):
        for h, a in permutations(team_ids, 2):
            self._probs_cache[(h, a)] = self.predict_fn(h, a)

    def simulate(
        self,
        groups: dict[str, list[Fixture]],
        _knockout_order: list = None,
        num_simulations: int | None = None,
    ) -> TournamentProjection:
        n = num_simulations or settings.simulation_count
        progress: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for _ in range(n):
            results = self._simulate_tournament(groups)
            for team_id, stage in results.items():
                progress[team_id][stage] += 1

        team_probs = []
        for team_id, stages in progress.items():
            tp = TeamTournamentProbability(
                team_id=team_id,
                champion_p=stages.get("champion", 0) / n,
                final_p=stages.get("final", 0) / n,
                semifinals_p=stages.get("semifinals", 0) / n,
                quarterfinals_p=stages.get("quarterfinals", 0) / n,
                round_of_16_p=stages.get("round_of_16", 0) / n,
                round_of_32_p=stages.get("round_of_32", 0) / n,
                win_group_p=stages.get("win_group", 0) / n,
                advance_p=stages.get("advance", 0) / n,
            )
            team_probs.append(tp)

        team_probs.sort(key=lambda x: x.champion_p, reverse=True)
        champion = team_probs[0].team_id if team_probs else ""

        return TournamentProjection(
            simulation_count=n,
            seed=settings.simulation_seed,
            team_probabilities=team_probs,
            most_likely_champion=champion,
        )

    def _simulate_tournament(
        self,
        groups: dict[str, list[Fixture]],
    ) -> dict[str, str]:
        results: dict[str, str] = {}
        group_winners: dict[str, str] = {}
        group_runners_up: dict[str, str] = {}
        third_placed: list[tuple[str, str, int, int, int]] = []

        for group_name, fixtures in groups.items():
            entries: dict[str, list[int]] = {}

            for f in fixtures:
                h_id, a_id = f.home_team_id, f.away_team_id
                if h_id not in entries:
                    entries[h_id] = [0, 0, 0, 0, 0, 0]
                if a_id not in entries:
                    entries[a_id] = [0, 0, 0, 0, 0, 0]

                if f.is_played and f.result:
                    hg, ag = f.result.home_goals, f.result.away_goals
                else:
                    hg, ag = self._sample_match(h_id, a_id)

                home = entries[h_id]
                away = entries[a_id]
                home[0] += 1
                away[0] += 1
                home[2] += hg
                home[3] += ag
                away[2] += ag
                away[3] += hg

                if hg > ag:
                    home[1] += 1
                    home[4] += 3
                    away[5] += 1
                elif hg == ag:
                    home[5] += 1
                    away[1] += 1
                    home[4] += 1
                    away[4] += 1
                else:
                    away[1] += 1
                    away[4] += 3
                    home[5] += 1

            sorted_teams = sorted(
                entries.items(),
                key=lambda x: (-x[1][4], -(x[1][2] - x[1][3]), -x[1][2]),
            )

            for i, (t_id, stats) in enumerate(sorted_teams):
                if i == 0:
                    group_winners[group_name] = t_id
                    results[t_id] = "win_group"
                elif i == 1:
                    group_runners_up[group_name] = t_id
                    results[t_id] = "advance"
                elif i == 2:
                    gd = stats[2] - stats[3]
                    third_placed.append((t_id, group_name, stats[4], gd, stats[2]))
                else:
                    results.setdefault(t_id, "group_stage")

        third_placed.sort(key=lambda x: (-x[2], -x[3], -x[4]))
        advancing_third = third_placed[:8]
        advancing_third_map: dict[str, str] = {}
        for t_id, group_letter, _, _, _ in advancing_third:
            advancing_third_map[group_letter] = t_id
            results[t_id] = "advance"

        r32_matches = self._build_r32_matches(
            group_winners, group_runners_up, advancing_third_map
        )
        self._simulate_bracket(r32_matches, results)
        return results

    def _build_r32_matches(
        self,
        group_winners: dict[str, str],
        group_runners_up: dict[str, str],
        advancing_third_map: dict[str, str],
    ) -> list[tuple[str | None, str | None]]:
        advancing_groups = sorted(advancing_third_map.keys())
        third_assignments = get_third_place_assignments(advancing_groups)

        def third(winner_group: str) -> str | None:
            tg = third_assignments.get(winner_group)
            return advancing_third_map.get(tg) if tg else None

        matches: list[tuple[str | None, str | None]] = [
            (group_runners_up.get("A"), group_runners_up.get("B")),      # M73
            (group_winners.get("E"), third("E")),                        # M74
            (group_winners.get("F"), group_runners_up.get("C")),         # M75
            (group_winners.get("C"), group_runners_up.get("F")),         # M76
            (group_winners.get("I"), third("I")),                        # M77
            (group_runners_up.get("E"), group_runners_up.get("I")),      # M78
            (group_winners.get("A"), third("A")),                        # M79
            (group_winners.get("L"), third("L")),                        # M80
            (group_winners.get("D"), third("D")),                        # M81
            (group_winners.get("G"), third("G")),                        # M82
            (group_runners_up.get("K"), group_runners_up.get("L")),      # M83
            (group_winners.get("H"), group_runners_up.get("J")),         # M84
            (group_winners.get("B"), third("B")),                        # M85
            (group_winners.get("J"), group_runners_up.get("H")),         # M86
            (group_winners.get("K"), third("K")),                        # M87
            (group_runners_up.get("D"), group_runners_up.get("G")),      # M88
        ]
        return matches

    def _simulate_bracket(
        self, r32_matches: list[tuple[str | None, str | None]], results: dict[str, str]
    ):
        r32_winners = []
        for home, away in r32_matches:
            winner = self._play_ko_match(home, away)
            r32_winners.append(winner)
            if winner:
                results[winner] = "round_of_32"

        r16_pairings = [
            (1, 4), (0, 2), (3, 5), (6, 7),
            (10, 11), (8, 9), (13, 15), (12, 14),
        ]
        r16_winners = []
        for i, j in r16_pairings:
            winner = self._play_ko_match(r32_winners[i], r32_winners[j])
            r16_winners.append(winner)
            if winner:
                results[winner] = "round_of_16"

        qf_pairings = [(0, 1), (2, 3), (4, 5), (6, 7)]
        qf_winners = []
        for i, j in qf_pairings:
            winner = self._play_ko_match(r16_winners[i], r16_winners[j])
            qf_winners.append(winner)
            if winner:
                results[winner] = "quarterfinals"

        sf_pairings = [(0, 1), (2, 3)]
        sf_winners = []
        for i, j in sf_pairings:
            winner = self._play_ko_match(qf_winners[i], qf_winners[j])
            sf_winners.append(winner)
            if winner:
                results[winner] = "semifinals"

        if len(sf_winners) >= 2 and sf_winners[0] and sf_winners[1]:
            champion = self._play_ko_match(sf_winners[0], sf_winners[1])
            if champion:
                results[champion] = "champion"

    def _play_ko_match(self, team_a: str | None, team_b: str | None) -> str | None:
        if team_a is None:
            return team_b
        if team_b is None:
            return team_a
        outcome = self._sample_match(team_a, team_b)
        goals_a, goals_b = outcome
        while goals_a == goals_b:
            outcome = self._sample_match(team_a, team_b)
            goals_a, goals_b = outcome
        return team_a if goals_a > goals_b else team_b

    def _sample_match(self, home_id: str, away_id: str) -> tuple[int, int]:
        key = (home_id, away_id)
        pred = self._probs_cache.get(key)
        if pred is None:
            pred = self.predict_fn(home_id, away_id)
            self._probs_cache[key] = pred

        lam_h = max(pred.expected_home_goals, 0.1)
        lam_a = max(pred.expected_away_goals, 0.1)
        home_g = int(self.rng.poisson(lam_h))
        away_g = int(self.rng.poisson(lam_a))
        return (min(home_g, 8), min(away_g, 8))

    def _next_stage(self, current: KnockoutStage) -> KnockoutStage:
        mapping = {
            KnockoutStage.ROUND_OF_32: KnockoutStage.ROUND_OF_16,
            KnockoutStage.ROUND_OF_16: KnockoutStage.QUARTERFINALS,
            KnockoutStage.QUARTERFINALS: KnockoutStage.SEMIFINALS,
            KnockoutStage.SEMIFINALS: KnockoutStage.FINAL,
            KnockoutStage.FINAL: KnockoutStage.FINAL,
        }
        return mapping[current]
