import json
import tempfile
import unittest
from pathlib import Path

from quiz import Quiz
from quiz_game import QuizGame


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.test_directory = Path(self.temporary_directory.name)

        self.game = QuizGame()
        self.game.state_path = self.test_directory / "state.json"
        self.game.use_default_state()

    def write_test_data(self, data):
        self.game.state_path.write_text(
            json.dumps(data, ensure_ascii=False),
            encoding="utf-8",
        )

    def assert_default_state(self):
        self.assertEqual(len(self.game.quizzes), 5)
        self.assertIsNone(self.game.best_score)

    def test_missing_file(self):
        self.assertFalse(self.game.state_path.exists())
        self.assertFalse(self.game.load_state())
        self.assert_default_state()

    def test_broken_json(self):
        broken_text = "{ invalid json"

        self.game.state_path.write_text(
            broken_text,
            encoding="utf-8",
        )
        self.game.best_score = 9

        self.assertFalse(self.game.load_state())
        self.assert_default_state()

        self.assertEqual(
            self.game.state_path.read_text(encoding="utf-8"),
            broken_text,
        )

    def test_invalid_data(self):
        invalid_cases = [
            [],
            {"quizzes": []},
            {"quizzes": "잘못된 목록", "best_score": None},
            {
                "quizzes": [
                    {
                        "question": "선택지 개수 오류",
                        "choices": ["1", "2", "3"],
                        "answer": 1,
                    }
                ],
                "best_score": None,
            },
            {
                "quizzes": [
                    {
                        "question": "정답 범위 오류",
                        "choices": ["1", "2", "3", "4"],
                        "answer": 5,
                    }
                ],
                "best_score": None,
            },
            {"quizzes": [], "best_score": -1},
            {"quizzes": [], "best_score": True},
        ]

        for data in invalid_cases:
            with self.subTest(data=data):
                self.write_test_data(data)
                self.assertFalse(self.game.load_state())
                self.assert_default_state()

    def test_empty_quizzes_and_zero_score(self):
        for score in (None, 0):
            with self.subTest(score=score):
                self.write_test_data(
                    {"quizzes": [], "best_score": score}
                )

                self.assertTrue(self.game.load_state())
                self.assertEqual(self.game.quizzes, [])
                self.assertEqual(self.game.best_score, score)

    def test_read_error(self):
        self.game.state_path.mkdir()

        self.assertFalse(self.game.load_state())
        self.assert_default_state()

    def test_write_error(self):
        self.game.state_path = (
            self.test_directory / "missing-directory" / "state.json"
        )

        self.assertFalse(self.game.save_state())
        self.assertFalse(self.game.state_path.exists())

    def test_save_and_reload(self):
        self.game.quizzes.append(
            Quiz(
                "[저장 검증용] 1+1은?",
                ["1", "2", "3", "4"],
                2,
            )
        )
        self.game.best_score = 3

        self.assertTrue(self.game.save_state())

        saved_text = self.game.state_path.read_text(encoding="utf-8")
        self.assertIn("저장 검증용", saved_text)

        restored_game = QuizGame()
        restored_game.state_path = self.game.state_path

        self.assertTrue(restored_game.load_state())
        self.assertEqual(len(restored_game.quizzes), 6)
        self.assertEqual(restored_game.best_score, 3)
        self.assertIsInstance(restored_game.quizzes[-1], Quiz)
        self.assertEqual(
            restored_game.quizzes[-1].question,
            "[저장 검증용] 1+1은?",
        )
        self.assertTrue(restored_game.quizzes[-1].check_answer(2))


if __name__ == "__main__":
    unittest.main(verbosity=2)