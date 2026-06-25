from src.models.tournament import KnockoutStage


class BracketBuilder:
    STAGE_ORDER = [
        KnockoutStage.ROUND_OF_32,
        KnockoutStage.ROUND_OF_16,
        KnockoutStage.QUARTERFINALS,
        KnockoutStage.SEMIFINALS,
        KnockoutStage.FINAL,
    ]

    @staticmethod
    def build_round_of_32(group_winners: list, group_runners_up: list, best_third: list) -> list:
        matches = []
        # WC2026 bracket: 12 group winners (GW) + 12 runners-up (RU) + 8 best third-placed (3rd)
        # Slots based on official WC2026 bracket structure
        slot_map = [
            ("1A", "2C"), ("1D", "2F"), ("1B", "2E"),
            ("1C", "2A"), ("1E", "2D"), ("1F", "2B"),
            ("1G", "3x"), ("1H", "3y"), ("1I", "3z"),
            ("1J", "3w"), ("1K", "2L"), ("1L", "2K"),
        ]
        return slot_map

    @staticmethod
    def resolve_knockout(
        home_team: str, away_team: str,
        sample_fn, stage: KnockoutStage
    ) -> str:
        result = sample_fn(home_team, away_team)
        if result["home_goals"] != result["away_goals"]:
            if result["home_goals"] > result["away_goals"]:
                return home_team
            return away_team
        # Penalty shootout: re-sample until resolved
        while result["home_goals"] == result["away_goals"]:
            result = sample_fn(home_team, away_team)
        return home_team if result["home_goals"] > result["away_goals"] else away_team
