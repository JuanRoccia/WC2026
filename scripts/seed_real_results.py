"""
Seed resultados reales del Mundial 2026 (actualizado al 25 de junio).
Busca cada fixture en los datos del sistema y carga el resultado.
Maneja casos donde home/away del fixture no coincide con el partido real.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.fixture import MatchResult
from src.services.prediction_service import PredictionService
from src.services.evaluation_service import EvaluationService

svc = PredictionService()
eval_svc = EvaluationService()

# Resultados reales: (grupo, team_a, team_b, goles_a, goles_b)
# team_a es el que figura como "local" en el resultado real
REAL_RESULTS = [
    # Grupo A
    ("A", "Mexico", "South Africa", 2, 0),
    ("A", "South Korea", "Czechia", 2, 1),
    ("A", "Czechia", "South Africa", 1, 1),
    ("A", "Mexico", "South Korea", 1, 0),
    ("A", "South Africa", "South Korea", 1, 0),
    ("A", "Czechia", "Mexico", 0, 3),
    # Grupo B
    ("B", "Canada", "Bosnia and Herzegovina", 1, 1),
    ("B", "Qatar", "Switzerland", 1, 1),
    ("B", "Switzerland", "Bosnia and Herzegovina", 4, 1),
    ("B", "Canada", "Qatar", 6, 0),
    ("B", "Bosnia and Herzegovina", "Qatar", 3, 1),
    ("B", "Switzerland", "Canada", 2, 1),
    # Grupo C
    ("C", "Brazil", "Morocco", 1, 1),
    ("C", "Haiti", "Scotland", 0, 1),
    ("C", "Scotland", "Morocco", 0, 1),
    ("C", "Brazil", "Haiti", 3, 0),
    ("C", "Morocco", "Haiti", 4, 2),
    ("C", "Scotland", "Brazil", 0, 3),
    # Grupo D
    ("D", "United States", "Paraguay", 4, 1),
    ("D", "Australia", "Turkey", 2, 0),
    ("D", "United States", "Australia", 2, 0),
    ("D", "Turkey", "Paraguay", 0, 1),
    # Grupo E
    ("E", "Germany", "Curacao", 7, 1),
    ("E", "Ivory Coast", "Ecuador", 1, 0),
    ("E", "Germany", "Ivory Coast", 2, 1),
    ("E", "Ecuador", "Curacao", 0, 0),
    # Grupo F
    ("F", "Netherlands", "Japan", 2, 2),
    ("F", "Sweden", "Tunisia", 5, 1),
    ("F", "Netherlands", "Sweden", 5, 1),
    ("F", "Tunisia", "Japan", 0, 4),
    # Grupo G
    ("G", "Egypt", "Belgium", 1, 1),
    ("G", "Iran", "New Zealand", 2, 2),
    ("G", "Belgium", "Iran", 0, 0),
    ("G", "New Zealand", "Egypt", 1, 3),
    # Grupo H
    ("H", "Spain", "Cape Verde", 0, 0),
    ("H", "Saudi Arabia", "Uruguay", 1, 1),
    ("H", "Spain", "Saudi Arabia", 4, 0),
    ("H", "Uruguay", "Cape Verde", 2, 2),
    # Grupo I
    ("I", "France", "Senegal", 3, 1),
    ("I", "Iraq", "Norway", 1, 4),
    ("I", "France", "Iraq", 3, 0),
    ("I", "Norway", "Senegal", 3, 2),
    # Grupo J
    ("J", "Argentina", "Algeria", 3, 0),
    ("J", "Austria", "Jordan", 3, 1),
    ("J", "Argentina", "Austria", 2, 0),
    ("J", "Jordan", "Algeria", 1, 2),
    # Grupo K
    ("K", "Portugal", "Congo DR", 1, 1),
    ("K", "Colombia", "Uzbekistan", 3, 1),
    ("K", "Portugal", "Uzbekistan", 5, 0),
    ("K", "Colombia", "Congo DR", 1, 0),
    # Grupo L
    ("L", "England", "Croatia", 4, 2),
    ("L", "Ghana", "Panama", 1, 0),
    ("L", "England", "Ghana", 0, 0),
    ("L", "Croatia", "Panama", 1, 0),
]

NAME_MAP = {
    "turkiye": "turkey",
    "turkive": "turkey",
    "dr_congo": "congo_dr",
}

def normalize(name):
    n = name.lower().replace(" ", "_")
    return NAME_MAP.get(n, n)

def find_fixture(svc, group_name, team_a, team_b):
    """Find fixture matching the real result, handling home/away swap."""
    id_a = normalize(team_a)
    id_b = normalize(team_b)
    for f in svc.data["fixtures"]:
        if f.group_name != group_name:
            continue
        if f.home_team_id == id_a and f.away_team_id == id_b:
            return f, False  # no swap
        if f.home_team_id == id_b and f.away_team_id == id_a:
            return f, True  # swap needed
    return None, False


count = 0
errors = []
for group, ta, tb, ga, gb in REAL_RESULTS:
    fixture, swapped = find_fixture(svc, group, ta, tb)
    if not fixture:
        errors.append(f"No fixture found: {group}: {ta} vs {tb}")
        continue
    if swapped:
        home_goals, away_goals = gb, ga
    else:
        home_goals, away_goals = ga, gb

    fixture.is_played = True
    fixture.result = MatchResult(home_goals=home_goals, away_goals=away_goals)

    pred = svc.predict_match(fixture.id)
    if pred and pred.best_prediction:
        eval_svc.evaluate(
            pred.best_prediction.outcome,
            home_goals, away_goals,
            predictor_name=pred.selected_predictor,
            fixture_id=fixture.id,
        )
    count += 1
    label = "OK" if not swapped else "SWAPPED"
    print(f"  [{label}] {fixture.id}: {fixture.home_team_name} {home_goals}-{away_goals} {fixture.away_team_name}")

svc.invalidate_direct_cache()

# Persist to JSON so results survive server restarts
from src.data.persistence import build_results_entries, save_results_json
save_results_json(build_results_entries(svc))

print(f"\nCargados {count} resultados.")
if errors:
    print(f"\nErrores ({len(errors)}):")
    for e in errors:
        print(f"  {e}")

print("\n--- Comparacion prediccion vs real ---")
for row in eval_svc.get_performance()[:5]:
    print(f"  {row.predictor_name}: Brier={row.avg_brier:.4f}, RPS={row.avg_rps:.4f}, Acc={row.top_pick_accuracy:.1%}")
