import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import read_int
from quiz_game import QuizGame


class TestAddQuiz(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.game = QuizGame()
        self.game.state_path = (
            Path(self.temporary_directory.name) / "state.json"
        )
        self.game.use_default_state()
        self.game.best_score = 2

        self.initial_count = len(self.game.quizzes)
        self.assertTrue(self.game.save_state())
        self.original_file = self.game.state_path.read_bytes()

    def run_add(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            return self.game.add_quiz(read_int)

    def read_saved_data(self):
        with self.game.state_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def assert_unchanged(self):
        self.assertEqual(len(self.game.quizzes), self.initial_count)
        self.assertEqual(self.game.best_score, 2)
        self.assertEqual(
            self.game.state_path.read_bytes(),
            self.original_file,
        )

    def test_valid_add_and_reload(self):
        result = self.run_add(
            ["검증용 새 문제", "보기1", "보기2", "보기3", "보기4", "1"]
        )

        self.assertTrue(result)
        self.assertEqual(len(self.game.quizzes), self.initial_count + 1)

        restored_game = QuizGame()
        restored_game.state_path = self.game.state_path

        self.assertTrue(restored_game.load_state())
        self.assertEqual(
            len(restored_game.quizzes),
            self.initial_count + 1,
        )
        self.assertEqual(
            restored_game.quizzes[-1].question,
            "검증용 새 문제",
        )
        self.assertEqual(restored_game.quizzes[-1].answer, 1)
        self.assertEqual(restored_game.best_score, 2)

    def test_blank_spaces_and_invalid_answer(self):
        result = self.run_add(
            [
                "",
                "   ",
                "  공백 검증 문제  ",
                "",
                "   ",
                "  보기1  ",
                "보기2",
                "보기3",
                "보기4",
                "abc",
                "",
                "0",
                "5",
                " 1 ",
            ]
        )

        self.assertTrue(result)

        quiz = self.game.quizzes[-1]
        self.assertEqual(quiz.question, "공백 검증 문제")
        self.assertEqual(quiz.choices, ["보기1", "보기2", "보기3", "보기4"])
        self.assertEqual(quiz.answer, 1)

        saved_data = self.read_saved_data()
        self.assertEqual(saved_data["best_score"], 2)
        self.assertEqual(
            len(saved_data["quizzes"]),
            self.initial_count + 1,
        )

    def test_keyboard_interrupt_keeps_state(self):
        with self.assertRaises(KeyboardInterrupt):
            self.run_add(
                ["미완성 문제", "보기1", KeyboardInterrupt]
            )

        self.assert_unchanged()

    def test_eof_keeps_state(self):
        with self.assertRaises(EOFError):
            self.run_add(
                ["미완성 문제", "보기1", "보기2", "보기3", "보기4", EOFError]
            )

        self.assert_unchanged()

    def test_save_failure_rolls_back(self):
        with patch.object(self.game, "save_state", return_value=False):
            result = self.run_add(
                ["저장 실패 문제", "보기1", "보기2", "보기3", "보기4", "2"]
            )

        self.assertFalse(result)
        self.assert_unchanged()

    def test_two_additions_keep_separate_choices(self):
        self.assertTrue(
            self.run_add(
                ["첫 문제", "가", "나", "다", "라", "1"]
            )
        )
        self.assertTrue(
            self.run_add(
                ["둘째 문제", "하나", "둘", "셋", "넷", "4"]
            )
        )

        self.assertEqual(len(self.game.quizzes), self.initial_count + 2)
        self.assertEqual(
            self.game.quizzes[-2].choices,
            ["가", "나", "다", "라"],
        )
        self.assertEqual(
            self.game.quizzes[-1].choices,
            ["하나", "둘", "셋", "넷"],
        )

        saved_data = self.read_saved_data()
        self.assertEqual(
            len(saved_data["quizzes"]),
            self.initial_count + 2,
        )
        self.assertEqual(saved_data["best_score"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)