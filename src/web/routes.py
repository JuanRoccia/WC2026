import json
import asyncio
import threading
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.services.prediction_service import PredictionService
from src.services.evaluation_service import EvaluationService
from src.services.data_service import DataService
from src.simulation.monte_carlo import MonteCarloSimulator
from src.config import settings
from src.data.persistence import load_results_json, apply_results, build_results_entries, save_results_json

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
pred_svc = PredictionService()
pred_svc.precompute_group_fixtures()

all_team_ids = list({t.id for g in pred_svc.data["groups"] for t in g.teams})

eval_svc = EvaluationService()
data_svc = DataService()

# Load persisted results so they survive restarts
saved = load_results_json()
if saved:
    apply_results(saved, pred_svc, eval_svc)
    pred_svc.invalidate_direct_cache()


@router.get("/")
async def root():
    return {"app": "WC2026 Predictor", "version": "0.1.0"}


# --- HTML UI routes ---

@router.get("/ui/", response_class=HTMLResponse)
async def ui_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "active": "home",
        "fixture_count": len(pred_svc.data["fixtures"]),
        "group_count": len(pred_svc.data["groups"]),
        "predictor_count": len(pred_svc.predictors),
    })


@router.get("/ui/fixtures", response_class=HTMLResponse)
async def ui_fixtures(request: Request):
    fixtures = []
    for f in pred_svc.data["fixtures"]:
        pred = pred_svc.predict_match(f.id)
        fixtures.append({
            "id": f.id,
            "group": f.group_name,
            "home_team": f.home_team_name,
            "away_team": f.away_team_name,
            "is_played": f.is_played,
            "result": {"home_goals": f.result.home_goals, "away_goals": f.result.away_goals} if f.result else None,
            "prediction": {
                "home_win": round(pred.best_prediction.outcome.home_win * 100, 1),
                "draw": round(pred.best_prediction.outcome.draw * 100, 1),
                "away_win": round(pred.best_prediction.outcome.away_win * 100, 1),
            } if pred and pred.best_prediction else None,
        })
    return templates.TemplateResponse("fixtures.html", {"request": request, "active": "fixtures", "fixtures": fixtures})


@router.get("/ui/fixtures/by-date", response_class=HTMLResponse)
async def ui_fixtures_by_date(request: Request, date: str | None = None):
    fixtures = []
    selected_date = date

    all_dates = sorted({
        f.kickoff.date() for f in pred_svc.data["fixtures"]
        if f.kickoff is not None
    })

    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")

        for f in pred_svc.data["fixtures"]:
            if f.kickoff and f.kickoff.date() == target_date:
                pred = pred_svc.predict_match(f.id)
                fixtures.append({
                    "id": f.id,
                    "group": f.group_name,
                    "home_team": f.home_team_name,
                    "away_team": f.away_team_name,
                    "kickoff": f.kickoff,
                    "is_played": f.is_played,
                    "result": {"home_goals": f.result.home_goals, "away_goals": f.result.away_goals} if f.result else None,
                    "prediction": {
                        "home_win": round(pred.best_prediction.outcome.home_win * 100, 1),
                        "draw": round(pred.best_prediction.outcome.draw * 100, 1),
                        "away_win": round(pred.best_prediction.outcome.away_win * 100, 1),
                    } if pred and pred.best_prediction else None,
                })

    return templates.TemplateResponse("fixtures_by_date.html", {
        "request": request,
        "active": "bydate",
        "fixtures": fixtures,
        "dates": [d.isoformat() for d in all_dates],
        "selected_date": selected_date,
    })


@router.get("/ui/fixtures/{fixture_id}", response_class=HTMLResponse)
async def ui_fixture_detail(request: Request, fixture_id: str):
    result = pred_svc.predict_match(fixture_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fixture not found")
    fixture = next((f for f in pred_svc.data["fixtures"] if f.id == fixture_id), None)
    detail = {
        "fixture_id": fixture_id,
        "home_team": fixture.home_team_name if fixture else "",
        "away_team": fixture.away_team_name if fixture else "",
        "selected_predictor": result.selected_predictor,
        "ladder": [
            {
                "predictor": p.predictor_name,
                "home_win": round(p.outcome.home_win * 100, 1),
                "draw": round(p.outcome.draw * 100, 1),
                "away_win": round(p.outcome.away_win * 100, 1),
                "is_degraded": p.is_degraded,
                "explanation": p.explanation,
            }
            for p in result.ladder
        ],
        "best_prediction": {
            "home_win": round(result.best_prediction.outcome.home_win * 100, 1),
            "draw": round(result.best_prediction.outcome.draw * 100, 1),
            "away_win": round(result.best_prediction.outcome.away_win * 100, 1),
            "expected_goals": {
                "home": round(result.best_prediction.expected_home_goals, 2),
                "away": round(result.best_prediction.expected_away_goals, 2),
            },
            "most_likely_score": result.best_prediction.most_likely_score,
        } if result.best_prediction else None,
    }
    return templates.TemplateResponse("fixture_detail.html", {"request": request, "active": "fixtures", "detail": detail, "fixture_id": fixture_id})


@router.get("/ui/groups", response_class=HTMLResponse)
async def ui_groups(request: Request):
    groups = data_svc.get_groups_summary()
    for g in groups:
        g["fixtures"] = []
        for f in pred_svc.data["fixtures"]:
            if f.group_name == g["name"]:
                g["fixtures"].append({
                    "id": f.id,
                    "home": f.home_team_name,
                    "away": f.away_team_name,
                })
    return templates.TemplateResponse("groups.html", {"request": request, "active": "groups", "groups": groups})


@router.get("/ui/simulation", response_class=HTMLResponse)
async def ui_simulation(request: Request):
    return templates.TemplateResponse("simulation.html", {
        "request": request,
        "active": "simulation",
    })


@router.get("/ui/performance", response_class=HTMLResponse)
async def ui_performance(request: Request):
    rows = eval_svc.get_performance()
    return templates.TemplateResponse("performance.html", {
        "request": request,
        "active": "performance",
        "performance": [r.model_dump() for r in rows],
    })


@router.get("/ui/lab", response_class=HTMLResponse)
async def ui_lab(request: Request):
    teams = data_svc.get_team_list()
    return templates.TemplateResponse("predictor_lab.html", {
        "request": request,
        "active": "lab",
        "teams": teams,
    })


@router.get("/ui/rankings", response_class=HTMLResponse)
async def ui_rankings(request: Request):
    elo = data_svc.get_elo_rankings()[:30]
    fifa = data_svc.get_fifa_rankings()[:30]
    return templates.TemplateResponse("rankings.html", {
        "request": request,
        "active": "rankings",
        "elo_rankings": elo,
        "fifa_rankings": fifa,
    })


# --- JSON API routes ---

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "fixtures": len(pred_svc.data["fixtures"]),
        "groups": len(pred_svc.data["groups"]),
        "predictors": len(pred_svc.predictors),
    }


@router.get("/fixtures")
async def get_fixtures():
    results = []
    for f in pred_svc.data["fixtures"]:
        pred = pred_svc.predict_match(f.id)
        results.append({
            "id": f.id,
            "group": f.group_name,
            "home_team": f.home_team_name,
            "away_team": f.away_team_name,
            "is_played": f.is_played,
            "result": {
                "home_goals": f.result.home_goals,
                "away_goals": f.result.away_goals,
            } if f.result else None,
            "prediction": {
                "home_win": round(pred.best_prediction.outcome.home_win * 100, 1),
                "draw": round(pred.best_prediction.outcome.draw * 100, 1),
                "away_win": round(pred.best_prediction.outcome.away_win * 100, 1),
                "selected_predictor": pred.selected_predictor,
                "most_likely_score": pred.best_prediction.most_likely_score,
            } if pred else None,
        })
    return {"fixtures": results}


@router.get("/fixtures/by-date")
async def get_fixtures_by_date(date: str):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    fixtures = []
    for f in pred_svc.data["fixtures"]:
        if f.kickoff and f.kickoff.date() == target_date:
            pred = pred_svc.predict_match(f.id)
            fixtures.append({
                "id": f.id,
                "group": f.group_name,
                "home_team": f.home_team_name,
                "away_team": f.away_team_name,
                "kickoff": f.kickoff.isoformat(),
                "is_played": f.is_played,
                "result": {
                    "home_goals": f.result.home_goals,
                    "away_goals": f.result.away_goals,
                } if f.result else None,
                "prediction": {
                    "home_win": round(pred.best_prediction.outcome.home_win * 100, 1),
                    "draw": round(pred.best_prediction.outcome.draw * 100, 1),
                    "away_win": round(pred.best_prediction.outcome.away_win * 100, 1),
                    "selected_predictor": pred.selected_predictor,
                    "most_likely_score": pred.best_prediction.most_likely_score,
                } if pred else None,
            })
    return {"date": date, "fixtures": fixtures}


@router.post("/fixtures/schedule/refresh")
async def refresh_fixtures_schedule(url: str | None = None):
    from src.data.loader import CsvLoader
    loader = CsvLoader()
    ok = loader.refresh_fixtures_schedule(url or settings.schedule_url)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to refresh schedule")
    schedule = loader.load_fixtures_schedule()
    if schedule:
        loader.apply_schedule(pred_svc.data["fixtures"], schedule)
        pred_svc.invalidate_direct_cache()
    return {"status": "ok", "fixtures_updated": len(schedule)}


@router.get("/fixtures/{fixture_id}")
async def get_fixture_detail(fixture_id: str):
    result = pred_svc.predict_match(fixture_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return {
        "fixture_id": result.fixture_id,
        "selected_predictor": result.selected_predictor,
        "ladder": [
            {
                "predictor": p.predictor_name,
                "home_win": round(p.outcome.home_win * 100, 1),
                "draw": round(p.outcome.draw * 100, 1),
                "away_win": round(p.outcome.away_win * 100, 1),
                "degraded": p.is_degraded,
                "explanation": p.explanation,
            }
            for p in result.ladder
        ],
        "best_prediction": {
            "home_win": round(result.best_prediction.outcome.home_win * 100, 1),
            "draw": round(result.best_prediction.outcome.draw * 100, 1),
            "away_win": round(result.best_prediction.outcome.away_win * 100, 1),
            "expected_goals": {
                "home": round(result.best_prediction.expected_home_goals, 2),
                "away": round(result.best_prediction.expected_away_goals, 2),
            },
            "most_likely_score": result.best_prediction.most_likely_score,
            "explanation": result.best_prediction.explanation,
        } if result.best_prediction else None,
    }


@router.get("/groups")
async def get_groups():
    groups = data_svc.get_groups_summary()
    for g in groups:
        g["fixtures"] = []
        for f in pred_svc.data["fixtures"]:
            if f.group_name == g["name"]:
                g["fixtures"].append({
                    "id": f.id,
                    "home": f.home_team_name,
                    "away": f.away_team_name,
                })
    return {"groups": groups}


@router.get("/predictor/lab")
async def predictor_lab(home: str, away: str):
    try:
        result = pred_svc.predict_direct(home, away)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    fixture = next((f for f in pred_svc.data["fixtures"]
                    if f.home_team_id == home and f.away_team_id == away), None)
    match_pred = pred_svc.predict_match(fixture.id) if fixture else None
    bp = match_pred.best_prediction if match_pred else None
    return {
        "home": home,
        "away": away,
        "home_win": round(result.home_win * 100, 1),
        "draw": round(result.draw * 100, 1),
        "away_win": round(result.away_win * 100, 1),
        "top_pick": result.top_pick,
        "expected_goals": {
            "home": round(bp.expected_home_goals, 2) if bp else None,
            "away": round(bp.expected_away_goals, 2) if bp else None,
        },
        "most_likely_score": list(bp.most_likely_score) if bp and bp.most_likely_score else None,
    }


@router.get("/simulation")
async def run_simulation(count: int | None = None):
    sim = MonteCarloSimulator(pred_svc.predict_direct, all_team_ids)

    groups: dict[str, list] = {}
    for f in pred_svc.data["fixtures"]:
        groups.setdefault(f.group_name, []).append(f)

    result = sim.simulate(groups, [], num_simulations=count)
    return {
        "simulation_count": result.simulation_count,
        "most_likely_champion": result.most_likely_champion,
        "team_probabilities": [
            {
                "team_id": tp.team_id,
                "champion_p": round(tp.champion_p * 100, 1),
                "final_p": round(tp.final_p * 100, 1),
                "semifinals_p": round(tp.semifinals_p * 100, 1),
                "quarterfinals_p": round(tp.quarterfinals_p * 100, 1),
            }
            for tp in sorted(result.team_probabilities, key=lambda x: -x.champion_p)[:20]
        ],
    }


@router.get("/simulation/stream")
async def simulation_stream(count: int = 100):
    async def event_generator():
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()

        def progress(phase: str, current: int, total: int):
            data = json.dumps({"phase": phase, "current": current, "total": total})
            loop.call_soon_threadsafe(queue.put_nowait, data)

        def run():
            sim = MonteCarloSimulator(pred_svc.predict_direct, all_team_ids, progress_callback=progress)
            groups: dict[str, list] = {}
            for f in pred_svc.data["fixtures"]:
                groups.setdefault(f.group_name, []).append(f)
            result = sim.simulate(groups, [], num_simulations=count)
            loop.call_soon_threadsafe(queue.put_nowait, None)
            return result

        sim_result: list = []
        def run_and_capture():
            sim_result.append(run())

        thread = threading.Thread(target=run_and_capture, daemon=True)
        thread.start()

        while True:
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=0.5)
                if msg is None:
                    break
                yield f"data: {msg}\n\n"
            except asyncio.TimeoutError:
                if not thread.is_alive():
                    break
                continue

        result = sim_result[0] if sim_result else None
        if result:
            team_probs = [
                {
                    "team_id": tp.team_id,
                    "champion_p": round(tp.champion_p * 100, 1),
                    "final_p": round(tp.final_p * 100, 1),
                    "semifinals_p": round(tp.semifinals_p * 100, 1),
                    "quarterfinals_p": round(tp.quarterfinals_p * 100, 1),
                }
                for tp in sorted(result.team_probabilities, key=lambda x: -x.champion_p)
            ]
            yield f"event: complete\ndata: {json.dumps({'simulation_count': result.simulation_count, 'most_likely_champion': result.most_likely_champion, 'team_probs': team_probs})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/fixtures/{fixture_id}/result")
async def set_result(fixture_id: str, home_goals: int, away_goals: int):
    fixture = next((f for f in pred_svc.data["fixtures"] if f.id == fixture_id), None)
    if not fixture:
        raise HTTPException(status_code=404, detail="Fixture not found")

    from src.models.fixture import MatchResult
    fixture.is_played = True
    fixture.result = MatchResult(home_goals=home_goals, away_goals=away_goals)

    pred = pred_svc.predict_match(fixture_id)
    if pred and pred.best_prediction:
        eval_svc.evaluate(
            pred.best_prediction.outcome,
            home_goals, away_goals,
            predictor_name=pred.selected_predictor,
            fixture_id=fixture_id,
        )

    save_results_json(build_results_entries(pred_svc))
    return {"status": "ok", "fixture_id": fixture_id}


@router.get("/performance")
async def get_performance():
    rows = eval_svc.get_performance()
    return {"performance": [r.model_dump() for r in rows]}


@router.get("/rankings/elo")
async def get_elo():
    return {"elo_rankings": data_svc.get_elo_rankings()[:30]}


@router.get("/rankings/fifa")
async def get_fifa():
    return {"fifa_rankings": data_svc.get_fifa_rankings()[:30]}
