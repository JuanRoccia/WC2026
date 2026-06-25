from pathlib import Path
import pandas as pd
from src.models.team import Team, Group
from src.models.fixture import Fixture
from src.models.rating import Rating, RatingType


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
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    fixtures.append(Fixture(
                        id=f"group_{group.name}_{fixture_id}",
                        group_name=group.name,
                        home_team_id=teams[i].id,
                        away_team_id=teams[j].id,
                        home_team_name=teams[i].name,
                        away_team_name=teams[j].name,
                    ))
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
