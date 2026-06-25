import numpy as np
from itertools import permutations
from collections import defaultdict
from src.config import settings
from src.models.fixture import Fixture
from src.models.tournament import (
    TournamentProjection, TeamTournamentProbability, KnockoutStage,
)
from src.services.prediction_service import DirectPrediction


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
        knockout_order: list,
        num_simulations: int | None = None,
    ) -> TournamentProjection:
        n = num_simulations or settings.simulation_count
        progress: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for _ in range(n):
            results = self._simulate_tournament(groups, knockout_order)
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
        knockout_order: list,
    ) -> dict[str, str]:
        results: dict[str, str] = {}
        group_winners: list[str] = []
        group_runners_up: list[str] = []
        best_third: list[tuple[str, int]] = []

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

            for i, (t_id, _) in enumerate(sorted_teams):
                if i == 0:
                    group_winners.append(t_id)
                    results[t_id] = "win_group"
                elif i == 1:
                    group_runners_up.append(t_id)
                    results[t_id] = "advance"
                elif i == 2:
                    gd = entries[t_id][2] - entries[t_id][3]
                    best_third.append((t_id, entries[t_id][4], gd, entries[t_id][2]))
                else:
                    results.setdefault(t_id, "group_stage")

        best_third.sort(key=lambda x: (-x[1], -x[2], -x[3]))
        advancing_third = [t[0] for t in best_third[:8]]

        for t_id in advancing_third:
            results[t_id] = "advance"

        knockout_teams = group_winners + group_runners_up + advancing_third
        self._simulate_knockout(knockout_teams, results)
        return results

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

    def _simulate_knockout(self, teams: list[str], results: dict[str, str]):
        stage = KnockoutStage.ROUND_OF_32
        remaining = teams[:32]

        while len(remaining) > 1:
            next_round = []
            for i in range(0, len(remaining), 2):
                if i + 1 >= len(remaining):
                    next_round.append(remaining[i])
                    break
                home, away = remaining[i], remaining[i + 1]
                outcome = self._sample_match(home, away)
                goals_h, goals_a = outcome
                while goals_h == goals_a:
                    outcome = self._sample_match(home, away)
                    goals_h, goals_a = outcome
                winner = home if goals_h > goals_a else away
                next_round.append(winner)
                stage_name = stage.value
                results[winner] = stage_name

            remaining = next_round
            stage = self._next_stage(stage)

        if remaining:
            results[remaining[0]] = "champion"

    def _next_stage(self, current: KnockoutStage) -> KnockoutStage:
        mapping = {
            KnockoutStage.ROUND_OF_32: KnockoutStage.ROUND_OF_16,
            KnockoutStage.ROUND_OF_16: KnockoutStage.QUARTERFINALS,
            KnockoutStage.QUARTERFINALS: KnockoutStage.SEMIFINALS,
            KnockoutStage.SEMIFINALS: KnockoutStage.FINAL,
            KnockoutStage.FINAL: KnockoutStage.FINAL,
        }
        return mapping[current]
