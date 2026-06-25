"""Tests para validar estructura del harness."""
from __future__ import annotations

import os
import unittest


class TestHarnessStructure(unittest.TestCase):
    """Validar que el harness tenga la estructura correcta."""

    def test_agents_directory_exists(self) -> None:
        """Directorio agents/ debe existir."""
        self.assertTrue(os.path.exists("agents"))
        self.assertTrue(os.path.isdir("agents"))

    def test_tasks_directory_exists(self) -> None:
        """Directorio tasks/ debe existir."""
        self.assertTrue(os.path.exists("tasks"))
        self.assertTrue(os.path.isdir("tasks"))

    def test_skills_directory_exists(self) -> None:
        """Directorio skills/ debe existir."""
        self.assertTrue(os.path.exists("skills"))
        self.assertTrue(os.path.isdir("skills"))

    def test_docs_directory_exists(self) -> None:
        """Directorio docs/ debe existir."""
        self.assertTrue(os.path.exists("docs"))
        self.assertTrue(os.path.isdir("docs"))

    def test_progress_directory_exists(self) -> None:
        """Directorio progress/ debe existir."""
        self.assertTrue(os.path.exists("progress"))
        self.assertTrue(os.path.isdir("progress"))

    def test_tests_directory_exists(self) -> None:
        """Directorio tests/ debe existir."""
        self.assertTrue(os.path.exists("tests"))
        self.assertTrue(os.path.isdir("tests"))

    def test_qa_directory_exists(self) -> None:
        """Directorio qa/ debe existir."""
        self.assertTrue(os.path.exists("qa"))
        self.assertTrue(os.path.isdir("qa"))

    def test_agents_md_exists(self) -> None:
        """AGENTS.md debe existir."""
        self.assertTrue(os.path.exists("AGENTS.md"))

    def test_feature_list_json_exists(self) -> None:
        """feature_list.json debe existir."""
        self.assertTrue(os.path.exists("feature_list.json"))

    def test_init_sh_exists(self) -> None:
        """init.sh debe existir."""
        self.assertTrue(os.path.exists("init.sh"))

    def test_agents_md_has_content(self) -> None:
        """AGENTS.md no debe estar vacío."""
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertGreater(len(content), 100)

    def test_docs_files_exist(self) -> None:
        """docs/ debe tener arquitecture.md, conventions.md, verification.md."""
        required_docs = [
            "docs/architecture.md",
            "docs/conventions.md",
            "docs/verification.md"
        ]
        for doc in required_docs:
            self.assertTrue(os.path.exists(doc), f"Falta: {doc}")

    def test_progress_files_exist(self) -> None:
        """progress/ debe tener current.md y history.md."""
        required_files = [
            "progress/current.md",
            "progress/history.md"
        ]
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Falta: {file}")

    def test_agent_files_exist(self) -> None:
        """agents/ debe tener los 7 archivos de agentes."""
        expected_agents = [
            "agents/01-arquitecto.md",
            "agents/02-code-reviewer.md",
            "agents/03-tester-debugger.md",
            "agents/04-frontend-ui.md",
            "agents/05-backend.md",
            "agents/06-ghost.md",
            "agents/07-qa-browser.md"
        ]
        for agent in expected_agents:
            self.assertTrue(os.path.exists(agent), f"Falta: {agent}")

    def test_task_files_exist(self) -> None:
        """tasks/ debe tener los 7 archivos de tareas."""
        expected_tasks = [
            "tasks/task-arquitecto.md",
            "tasks/task-code-reviewer.md",
            "tasks/task-tester.md",
            "tasks/task-frontend.md",
            "tasks/task-backend.md",
            "tasks/task-ghost.md",
            "tasks/task-qa-browser.md"
        ]
        for task in expected_tasks:
            self.assertTrue(os.path.exists(task), f"Falta: {task}")


class TestSpecsStructure(unittest.TestCase):
    """Validar que la capa specs tenga la estructura correcta."""

    def test_specs_template_exists(self) -> None:
        """specs/_template.md debe existir."""
        self.assertTrue(os.path.exists("specs/_template.md"))

    def test_specs_readme_exists(self) -> None:
        """specs/_README.md debe existir."""
        self.assertTrue(os.path.exists("specs/_README.md"))

    def test_specs_example_complete(self) -> None:
        """specs/example/ debe tener spec.md, changelog.md y decisions.md."""
        expected = [
            "specs/example/spec.md",
            "specs/example/changelog.md",
            "specs/example/decisions.md"
        ]
        for file in expected:
            self.assertTrue(os.path.exists(file), f"Falta: {file}")

    def test_qa_files_exist(self) -> None:
        """qa/ debe tener runner, register, setup y README."""
        expected = [
            "qa/qa-runner.mjs",
            "qa/qa-register.mjs",
            "qa/setup-qa-local.sh",
            "qa/README.md"
        ]
        for file in expected:
            self.assertTrue(os.path.exists(file), f"Falta: {file}")


if __name__ == "__main__":
    unittest.main()
