import json
import unittest
from unittest.mock import patch

from automate import Automate
from main import collect_automation_mode
from reasoning import Reason


class StubReason:
    def __init__(self, verify_results, regenerated_plan):
        self.verify_results = list(verify_results)
        self.regenerated_plan = regenerated_plan
        self.feedback_messages = []

    def _call_model(self, prompt):
        return self.verify_results.pop(0)

    def step_verification_prompt(self, step):
        return f"verify:{step['step']}"

    def clean_data(self, raw):
        return json.loads(raw)

    def generate_plan(self, feedback=None):
        self.feedback_messages.append(feedback)
        return self.regenerated_plan


class ValidatePlanTests(unittest.TestCase):
    def test_validate_plan_accepts_valid_steps(self):
        plan = [
            {
                "id": 1,
                "step": "Open the app",
                "action": [{"keyword": "press", "key": "win"}],
            }
        ]

        Automate.validate_plan(plan)

    def test_validate_plan_rejects_non_list(self):
        with self.assertRaisesRegex(ValueError, "Plan must be a list"):
            Automate.validate_plan({"step": "bad"})

    def test_validate_plan_requires_keyword(self):
        plan = [{"id": 1, "step": "Broken step", "action": [{}]}]

        with self.assertRaisesRegex(ValueError, "missing 'keyword'"):
            Automate.validate_plan(plan)


class CleanDataTests(unittest.TestCase):
    def setUp(self):
        self.reason = Reason("test task")

    def test_clean_data_parses_fenced_verification_json(self):
        raw = '```json\n{"status": "ok", "reason": ""}\n```'

        result = self.reason.clean_data(raw)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["reason"], "")

    def test_clean_data_removes_trailing_commas_from_plan(self):
        raw = """
        ```json
        [
          {
            "id": 1,
            "step": "Click search",
            "action": [
              {"keyword": "click"},
            ],
          },
        ]
        ```
        """

        result = self.reason.clean_data(raw)

        self.assertEqual(result[0]["step"], "Click search")
        self.assertEqual(result[0]["action"][0]["keyword"], "click")


class AutomationModeSelectionTests(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", return_value="")
    def test_collect_automation_mode_defaults_to_simple(self, mocked_input, mocked_print):
        self.assertEqual(collect_automation_mode(), "simple")

    @patch("builtins.print")
    @patch("builtins.input", return_value="2")
    def test_collect_automation_mode_accepts_advanced_shortcut(self, mocked_input, mocked_print):
        self.assertEqual(collect_automation_mode(), "advanced")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["wrong", "advanced"])
    def test_collect_automation_mode_retries_after_invalid_choice(self, mocked_input, mocked_print):
        self.assertEqual(collect_automation_mode(), "advanced")


class AutomateRetryTests(unittest.TestCase):
    def test_run_simple_executes_plan_without_verification(self):
        plan = [
            {
                "id": 1,
                "step": "Simple attempt",
                "action": [{"keyword": "wait", "duration": 0}],
            }
        ]

        with patch.object(Automate, "_execute_action", autospec=True) as execute_action:
            Automate().run(plan, mode="simple")

        self.assertEqual(execute_action.call_count, 1)

    def test_automate_retries_after_failed_verification(self):
        initial_plan = [
            {
                "id": 1,
                "step": "Initial attempt",
                "action": [{"keyword": "wait", "duration": 0}],
            }
        ]
        regenerated_plan = [
            {
                "id": 1,
                "step": "Retry attempt",
                "action": [{"keyword": "wait", "duration": 0}],
            }
        ]
        reason = StubReason(
            verify_results=[
                '{"status": "fail", "reason": "target not reached"}',
                '{"status": "ok", "reason": ""}',
            ],
            regenerated_plan=regenerated_plan,
        )

        with patch.object(Automate, "_execute_action", autospec=True) as execute_action:
            Automate().automate(initial_plan, reason)

        self.assertEqual(execute_action.call_count, 2)
        self.assertEqual(len(reason.feedback_messages), 1)
        self.assertIn("target not reached", reason.feedback_messages[0])


if __name__ == "__main__":
    unittest.main()
