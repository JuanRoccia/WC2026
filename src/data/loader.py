from datetime import date, datetime
from pathlib import Path
import pandas as pd
from src.models.team import Team, Group
from src.models.fixture import Fixture
from src.models.rating import Rating, RatingType


# WC2026 group stage schedule: (round1, round2, round3) per group
# Matchday 1: Jun 11-17, Matchday 2: Jun 18-23, Matchday 3: Jun 24-27
_GROUP_MATCHDAY_DATES: dict[str, tuple[date, date, date]] = {
    "A": (date(2026, 6, 11), date(2026, 6, 17), date(2026, 6, 24)),
    "B": (date(2026, 6, 12), date(2026, 6, 18), date(2026, 6, 24)),
    "C": (date(2026, 6, 13), date(2026, 6, 19), date(2026, 6, 25)),
    "D": (date(2026, 6, 12), date(2026, 6, 19), date(2026, 6, 25)),
    "E": (date(2026, 6, 13), date(2026, 6, 20), date(2026, 6, 25)),
    "F": (date(2026, 6, 14), date(2026, 6, 20), date(2026, 6, 26)),
    "G": (date(2026, 6, 14), date(2026, 6, 21), date(2026, 6, 26)),
    "H": (date(2026, 6, 15), date(2026, 6, 21), date(2026, 6, 26)),
    "I": (date(2026, 6, 15), date(2026, 6, 22), date(2026, 6, 27)),
    "J": (date(2026, 6, 16), date(2026, 6, 22), date(2026, 6, 27)),
    "K": (date(2026, 6, 16), date(2026, 6, 23), date(2026, 6, 27)),
    "L": (date(2026, 6, 17), date(2026, 6, 23), date(2026, 6, 27)),
}


def _matchday(local_idx: int) -> int:
    """Map fixture index within group (0-5) to matchday (1, 2, or 3)."""
    return {0: 1, 1: 2, 2: 3, 3: 3, 4: 2, 5: 1}[local_idx]


class CsvLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def load_groups(self, filename: str = "wc2026_groups.csv") -> list[Group]:
        df = pd.read_csv(self.data_dir / filename)
        groups: dict[str, Group] = {}
        for _, row in df.iterrows():
            group_name = row["group"]
            if group_name not in groups:
                groups[group_name] = Group(name=group_name, teams=[])
            team = Team(
                id=row["team"].lower().replace(" ", "_"),
                name=row["team"],
                flag_code=str(row.get("flag", "")),
            )
            groups[group_name].teams.append(team)
        return list(groups.values())

    def load_historical_results(self, filename: str = "historical_results.csv") -> pd.DataFrame:
        return pd.read_csv(
            self.data_dir / filename,
            parse_dates=["date"],
            date_format="mixed",
        )

    def load_elo_ratings(self, filename: str = "elo_snapshot.csv") -> list[Rating]:
        df = pd.read_csv(self.data_dir / filename)
        return [
            Rating(
                team_id=row["team"].lower().replace(" ", "_"),
                rating_type=RatingType.ELO,
                value=float(row["elo_rating"]),
                rank=int(row.get("rank", 0)),
            )
            for _, row in df.iterrows()
        ]

    def load_fifa_rankings(self, filename: str = "fifa_rankings.csv") -> list[Rating]:
        df = pd.read_csv(self.data_dir / filename)
        return [
            Rating(
                team_id=row["team"].lower().replace(" ", "_"),
                rating_type=RatingType.FIFA,
                value=float(row["points"]),
                rank=int(row.get("rank", 0)),
            )
            for _, row in df.iterrows()
        ]

    def load_goalscorers(self, filename: str = "goalscorers.csv") -> pd.DataFrame:
        return pd.read_csv(
            self.data_dir / filename,
            parse_dates=["date"],
            date_format="mixed",
        )

    def generate_fixtures(self, groups: list[Group]) -> list[Fixture]:
        fixtures: list[Fixture] = []
        fixture_id = 1
        for group in groups:
            teams = group.teams
            group_dates = _GROUP_MATCHDAY_DATES.get(group.name)
            for idx, (i, j) in enumerate([(i, j) for i in range(len(teams)) for j in range(i + 1, len(teams))]):
                f = Fixture(
                    id=f"group_{group.name}_{fixture_id}",
                    group_name=group.name,
                    home_team_id=teams[i].id,
                    away_team_id=teams[j].id,
                    home_team_name=teams[i].name,
                    away_team_name=teams[j].name,
                )
                if group_dates:
                    md = _matchday(idx)
                    f.kickoff = datetime.combine(group_dates[md - 1], datetime.min.time())
                fixtures.append(f)
                fixture_id += 1
        return fixtures


def load_all_data(data_dir: str = "data") -> dict:
    loader = CsvLoader(data_dir)
    groups = loader.load_groups()
    elo_ratings = loader.load_elo_ratings()
    fifa_ratings = loader.load_fifa_rankings()
    historical = loader.load_historical_results()
    fixtures = loader.generate_fixtures(groups)
    return {
        "groups": groups,
        "fixtures": fixtures,
        "elo_ratings": {r.team_id: r for r in elo_ratings},
        "fifa_ratings": {r.team_id: r for r in fifa_ratings},
        "historical": historical,
    }
