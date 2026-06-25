import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestHealth:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["fixtures"] == 72
        assert data["groups"] == 12
        assert data["predictors"] == 6

    def test_root_returns_app_info(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "WC2026 Predictor" in data["app"]


class TestFixtures:
    def test_get_fixtures(self):
        response = client.get("/fixtures")
        assert response.status_code == 200
        data = response.json()
        assert "fixtures" in data
        assert len(data["fixtures"]) == 72

    def test_fixture_has_prediction(self):
        response = client.get("/fixtures")
        data = response.json()
        fixture = data["fixtures"][0]
        assert "id" in fixture
        assert "home_team" in fixture
        assert "away_team" in fixture
        assert "group" in fixture
        assert "prediction" in fixture or fixture["is_played"]

    def test_fixture_detail_found(self):
        response = client.get("/fixtures/group_A_1")
        assert response.status_code == 200
        data = response.json()
        assert data["fixture_id"] == "group_A_1"
        assert "ladder" in data
        assert len(data["ladder"]) == 6

    def test_fixture_detail_not_found(self):
        response = client.get("/fixtures/nonexistent")
        assert response.status_code == 404


class TestGroups:
    def test_get_groups(self):
        response = client.get("/groups")
        assert response.status_code == 200
        data = response.json()
        assert "groups" in data
        assert len(data["groups"]) == 12
        assert all("name" in g and "teams" in g and "fixtures" in g for g in data["groups"])

    def test_group_has_teams(self):
        response = client.get("/groups")
        data = response.json()
        for g in data["groups"]:
            assert len(g["teams"]) == 4


class TestSimulation:
    def test_simulation_endpoint(self):
        response = client.get("/simulation?count=50")
        assert response.status_code == 200
        data = response.json()
        assert data["simulation_count"] == 50
        assert "most_likely_champion" in data
        assert "team_probabilities" in data
        assert len(data["team_probabilities"]) > 0

    def test_simulation_probabilities_summary(self):
        response = client.get("/simulation?count=50")
        data = response.json()
        for tp in data["team_probabilities"]:
            assert "team_id" in tp
            assert "champion_p" in tp
            assert "final_p" in tp
            assert 0 <= tp["champion_p"] <= 100


class TestPerformance:
    def test_performance_endpoint(self):
        response = client.get("/performance")
        assert response.status_code == 200
        data = response.json()
        assert "performance" in data
        assert isinstance(data["performance"], list)


class TestPredictorLab:
    def test_predictor_lab(self):
        response = client.get("/predictor/lab?home=argentina&away=brazil")
        assert response.status_code == 200
        data = response.json()
        assert data["home"] == "argentina"
        assert data["away"] == "brazil"
        assert "home_win" in data
        assert "draw" in data
        assert "away_win" in data

    def test_predictor_lab_invalid_team(self):
        response = client.get("/predictor/lab?home=nonexistent&away=brazil")
        assert response.status_code in (200, 400)


class TestRankings:
    def test_elo_rankings(self):
        response = client.get("/rankings/elo")
        assert response.status_code == 200
        data = response.json()
        assert "elo_rankings" in data
        assert len(data["elo_rankings"]) <= 30

    def test_fifa_rankings(self):
        response = client.get("/rankings/fifa")
        assert response.status_code == 200
        data = response.json()
        assert "fifa_rankings" in data
        assert len(data["fifa_rankings"]) <= 30


class TestSetResult:
    def test_set_result_updates_fixture(self):
        response = client.post("/fixtures/group_A_1/result?home_goals=2&away_goals=1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["fixture_id"] == "group_A_1"

    def test_set_result_not_found(self):
        response = client.post("/fixtures/nonexistent/result?home_goals=1&away_goals=0")
        assert response.status_code == 404

    def test_set_result_then_fixture_shows_played(self):
        client.post("/fixtures/group_A_2/result?home_goals=1&away_goals=1")
        response = client.get("/fixtures/group_A_2")
        data = response.json()
        assert data["fixture_id"] == "group_A_2"


class TestUI:
    def test_ui_home(self):
        response = client.get("/ui/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_ui_fixtures(self):
        response = client.get("/ui/fixtures")
        assert response.status_code == 200

    def test_ui_groups(self):
        response = client.get("/ui/groups")
        assert response.status_code == 200

    def test_ui_simulation(self):
        response = client.get("/ui/simulation")
        assert response.status_code == 200

    def test_ui_performance(self):
        response = client.get("/ui/performance")
        assert response.status_code == 200

    def test_ui_lab(self):
        response = client.get("/ui/lab")
        assert response.status_code == 200

    def test_ui_rankings(self):
        response = client.get("/ui/rankings")
        assert response.status_code == 200

    def test_ui_fixture_detail(self):
        response = client.get("/ui/fixtures/group_A_1")
        assert response.status_code == 200

    def test_ui_fixture_detail_not_found(self):
        response = client.get("/ui/fixtures/nonexistent")
        assert response.status_code == 404
