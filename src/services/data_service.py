from src.data.loader import CsvLoader


class DataService:
    def __init__(self, data_dir: str = "data"):
        self.loader = CsvLoader(data_dir)

    def get_groups_summary(self) -> list[dict]:
        groups = self.loader.load_groups()
        return [
            {
                "name": g.name,
                "teams": [{"id": t.id, "name": t.name} for t in g.teams],
            }
            for g in groups
        ]

    def get_team_list(self) -> list[dict]:
        groups = self.loader.load_groups()
        teams = []
        for g in groups:
            for t in g.teams:
                teams.append({"id": t.id, "name": t.name, "group": g.name})
        return sorted(teams, key=lambda x: x["name"])

    def get_elo_rankings(self) -> list[dict]:
        ratings = self.loader.load_elo_ratings()
        return sorted(
            [{"team": r.team_id, "rating": r.value, "rank": r.rank} for r in ratings],
            key=lambda x: -x["rating"],
        )

    def get_fifa_rankings(self) -> list[dict]:
        ratings = self.loader.load_fifa_rankings()
        return sorted(
            [{"team": r.team_id, "points": r.value, "rank": r.rank} for r in ratings],
            key=lambda x: x["rank"],
        )
