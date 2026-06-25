"""Tests para validar feature_list.json."""
from __future__ import annotations

import json
import os
import unittest


class TestFeatureList(unittest.TestCase):
    """Validar estructura de feature_list.json."""

    def setUp(self) -> None:
        self.feature_list_path = "feature_list.json"
        with open(self.feature_list_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_file_exists(self) -> None:
        """feature_list.json debe existir."""
        self.assertTrue(os.path.exists(self.feature_list_path))

    def test_valid_json(self) -> None:
        """Debe ser JSON válido."""
        try:
            with open(self.feature_list_path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"JSON inválido: {e}")

    def test_has_required_keys(self) -> None:
        """Debe tener 'project' y 'features'."""
        self.assertIn("project", self.data)
        self.assertIn("features", self.data)

    def test_features_is_list(self) -> None:
        """'features' debe ser una lista."""
        self.assertIsInstance(self.data["features"], list)

    def test_features_not_empty(self) -> None:
        """Debe tener al menos una feature."""
        self.assertGreater(len(self.data["features"]), 0)

    def test_feature_has_required_fields(self) -> None:
        """Cada feature debe tener id, name, title, status."""
        required = {"id", "name", "title", "status"}
        for feature in self.data["features"]:
            self.assertTrue(required.issubset(feature.keys()),
                            f"Falta campos en feature: {feature}")

    def test_valid_status_values(self) -> None:
        """Status debe ser pending/in_progress/done/blocked."""
        valid = {"pending", "in_progress", "done", "blocked"}
        for feature in self.data["features"]:
            self.assertIn(feature["status"], valid,
                         f"Status inválido: {feature['status']}")

    def test_max_one_in_progress(self) -> None:
        """Máximo una feature en in_progress."""
        in_progress = [f for f in self.data["features"]
                      if f["status"] == "in_progress"]
        self.assertLessEqual(len(in_progress), 1)


if __name__ == "__main__":
    unittest.main()
