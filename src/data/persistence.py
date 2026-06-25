"""Save/load fixture results to JSON for restart persistence."""
import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent.parent.parent / "data" / "results.json"


def load_results_json(path=None) -> list[dict]:
    if path is not None:
        path = Path(path)
    else:
        path = DEFAULT_PATH
    if not path.exists():
        return []
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def apply_results(entries: list[dict], pred_svc, eval_svc):
    """Apply saved fixture results + re-evaluate predictions."""
    from src.models.fixture import MatchResult

    for entry in entries:
        fixture = next(
            (f for f in pred_svc.data["fixtures"] if f.id == entry["fixture_id"]),
            None,
        )
        if not fixture:
            continue
        fixture.is_played = True
        fixture.result = MatchResult(
            home_goals=entry["home_goals"], away_goals=entry["away_goals"]
        )
        # Re-evaluate prediction against actual result
        pred = pred_svc.predict_match(fixture.id)
        if pred and pred.best_prediction:
            eval_svc.evaluate(
                pred.best_prediction.outcome,
                entry["home_goals"],
                entry["away_goals"],
                predictor_name=pred.selected_predictor,
                fixture_id=fixture.id,
            )


def build_results_entries(pred_svc) -> list[dict]:
    """Build list of {fixture_id, home_goals, away_goals} from played fixtures."""
    entries = []
    for f in pred_svc.data["fixtures"]:
        if not f.is_played or not f.result:
            continue
        entries.append({
            "fixture_id": f.id,
            "home_goals": f.result.home_goals,
            "away_goals": f.result.away_goals,
        })
    return entries


def save_results_json(entries: list[dict], path=None):
    if path is not None:
        path = Path(path)
    else:
        path = DEFAULT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(entries, f, indent=2)
