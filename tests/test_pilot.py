import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jev_pilot import JevPilot, DecisionResult, SafetyResult, StuckResult, FactResult

API_KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")

class TestJevPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not API_KEY:
            raise unittest.SkipTest("Skipping live API tests: TYPESAFE_API_KEY environment variable not set.")
        cls.pilot = JevPilot(api_key=API_KEY)

    def test_arbitrate(self):
        context = "Need to parse unstructured date strings ('tomorrow at 5pm') into ISO 8601 in Python."
        candidates = {
            "regex": "Write huge custom regular expressions manually",
            "dateutil": "Use python-dateutil / dateparser library",
            "llm_call": "Send every date string to an LLM API"
        }
        res = self.pilot.arbitrate(context, candidates)
        self.assertIsInstance(res, DecisionResult)
        self.assertEqual(res.winner, "dateutil")
        self.assertGreater(res.confidence, 0.5)
        self.assertLess(res.latency, 1.0)

    def test_guard_destructive(self):
        action = "rm -rf /var/lib/mysql/*"
        state = "Production database server active"
        res = self.pilot.guard(action, state)
        self.assertIsInstance(res, SafetyResult)
        self.assertFalse(res.allowed)
        self.assertGreater(res.danger_score, 0.7)
        self.assertEqual(res.action_type, "destructive")

    def test_guard_safe(self):
        action = "git status"
        state = "Checking git repository changes"
        res = self.pilot.guard(action, state)
        self.assertIsInstance(res, SafetyResult)
        self.assertTrue(res.allowed)
        self.assertLess(res.danger_score, 0.2)

    def test_check_stuck(self):
        history = [
            "terminal('curl http://localhost:8080') -> Connection refused",
            "terminal('curl http://localhost:8080') -> Connection refused",
            "terminal('curl http://localhost:8080') -> Connection refused",
            "terminal('curl http://localhost:8080') -> Connection refused"
        ]
        res = self.pilot.check_stuck(history)
        self.assertIsInstance(res, StuckResult)
        self.assertTrue(res.is_stuck)
        self.assertGreater(res.confidence, 0.7)

    def test_verify_fact_hallucination(self):
        ground_truth = "The speed of light in vacuum is approximately 299,792,458 meters per second."
        claim = "The speed of light in vacuum is approximately 50,000 meters per second."
        res = self.pilot.verify_fact(claim, ground_truth)
        self.assertIsInstance(res, FactResult)
        self.assertTrue(res.is_hallucination)

    def test_route(self):
        res = self.pilot.route(
            prompt="Write a quicksort implementation in Rust",
            routes={
                "coding": "Coding tasks, algorithms, programming languages",
                "cooking": "Culinary recipes and kitchen advice"
            }
        )
        self.assertEqual(res["route"], "coding")
        self.assertGreater(res["confidence"], 0.8)

if __name__ == "__main__":
    unittest.main()
