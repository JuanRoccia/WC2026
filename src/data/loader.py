from datetime import datetime
from pathlib import Path
import json
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

    def load_fixtures_schedule(self, filename: str = "fixtures_schedule.json") -> list[dict]:
        path = self.data_dir / filename
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def apply_schedule(self, fixtures: list[Fixture], schedule: list[dict]):
        schedule_map: dict[tuple[str, str, str], dict] = {}
        for entry in schedule:
            key = (entry["group"], entry["home_team"], entry["away_team"])
            schedule_map[key] = entry

        for f in fixtures:
            direct = schedule_map.get((f.group_name, f.home_team_name, f.away_team_name))
            swapped = schedule_map.get((f.group_name, f.away_team_name, f.home_team_name))
            entry = direct or swapped
            if entry:
                f.kickoff = datetime.fromisoformat(entry["date"])
                f.venue = entry.get("venue", "")

    def refresh_fixtures_schedule(self, url: str | None = None, filename: str = "fixtures_schedule.json") -> bool:
        if not url:
            return False
        try:
            import requests
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            path = self.data_dir / filename
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False


def load_all_data(data_dir: str = "data") -> dict:
    loader = CsvLoader(data_dir)
    groups = loader.load_groups()
    elo_ratings = loader.load_elo_ratings()
    fifa_ratings = loader.load_fifa_rankings()
    historical = loader.load_historical_results()
    fixtures = loader.generate_fixtures(groups)
    schedule = loader.load_fixtures_schedule()
    if schedule:
        loader.apply_schedule(fixtures, schedule)
    return {
        "groups": groups,
        "fixtures": fixtures,
        "elo_ratings": {r.team_id: r for r in elo_ratings},
        "fifa_ratings": {r.team_id: r for r in fifa_ratings},
        "historical": historical,
    }
