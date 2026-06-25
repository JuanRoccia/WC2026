from src.models.tournament import GroupTableEntry
from src.models.fixture import Fixture


class GroupTableCalculator:
    @staticmethod
    def calculate(fixtures: list[Fixture]) -> list[GroupTableEntry]:
        entries: dict[str, GroupTableEntry] = {}

        for f in fixtures:
            for team_id in [f.home_team_id, f.away_team_id]:
                if team_id not in entries:
                    entries[team_id] = GroupTableEntry(
                        team_id=team_id,
                        team_name=f.home_team_name if team_id == f.home_team_id else f.away_team_name,
                    )

            if f.is_played and f.result:
                hg, ag = f.result.home_goals, f.result.away_goals
                home = entries[f.home_team_id]
                away = entries[f.away_team_id]

                home.played += 1
                away.played += 1
                home.goals_for += hg
                home.goals_against += ag
                away.goals_for += ag
                away.goals_against += hg

                if hg > ag:
                    home.won += 1
                    home.points += 3
                    away.lost += 1
                elif hg == ag:
                    home.drawn += 1
                    away.drawn += 1
                    home.points += 1
                    away.points += 1
                else:
                    away.won += 1
                    away.points += 3
                    home.lost += 1

        return sorted(
            entries.values(),
            key=lambda e: (-e.points, -(e.goals_for - e.goals_against), -e.goals_for),
        )

    @staticmethod
    def resolve_tiebreaker(a: GroupTableEntry, b: GroupTableEntry, h2h: dict[str, int]) -> int:
        if a.points != b.points:
            return -1 if a.points > b.points else 1
        gd_a = a.goals_for - a.goals_against
        gd_b = b.goals_for - b.goals_against
        if gd_a != gd_b:
            return -1 if gd_a > gd_b else 1
        if a.goals_for != b.goals_for:
            return -1 if a.goals_for > b.goals_for else 1
        h2h_a = h2h.get(a.team_id, 0)
        h2h_b = h2h.get(b.team_id, 0)
        if h2h_a != h2h_b:
            return -1 if h2h_a > h2h_b else 1
        return 0
