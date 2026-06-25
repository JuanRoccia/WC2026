from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    simulation_count: int = 10000
    simulation_seed: int = 2026
    recent_result_count: int = 8
    goal_model_years_window: int = 4
    goal_strength_min: float = 0.25
    goal_strength_max: float = 3.5
    goal_prior_matches: float = 2.0
    goal_iterations: int = 8
    goal_decay_factor: float = 0.75
    home_advantage: float = 1.08
    dixon_coles_rho: float = 0.00
    elo_draw_base: float = 0.30
    elo_draw_min: float = 0.08
    ranking_calibration_weight: float = 0.15
    form_recent_weight: float = 0.8
    db_path: str = str(Path(__file__).parent.parent / "data" / "wc2026.db")
    data_dir: str = str(Path(__file__).parent.parent / "data")
    results_file: str = str(Path(__file__).parent.parent / "data" / "results.json")

    class Config:
        env_prefix = "WC2026_"
        env_file = ".env"


settings = Settings()
