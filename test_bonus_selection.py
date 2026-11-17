import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import read_int
from quiz import Quiz
from quiz_game import QuizGame


class TestBonusSelection(unittest.TestCase):
    def setUp(self):
        self.game = QuizGame.__new__(QuizGame)
        self.game.quizzes = [
            Quiz(
                f"시험 문제 {number}",
                ["정답", "보기2", "보기3", "보기4"],
                1,
            )
            for number in range(1, 5)
        ]

    def test_selected_order_and_count(self):
        """선택 함수의 결과 순서와 개수를 실제 출제에 사용한다."""
        original = list(self.game.quizzes)
        selected = [original[3], original[1]]
        reader = unittest.mock.Mock(side_effect=[2, 1, 1])
        displayed = []

        with patch(
            "quiz_game.random.sample", return_value=selected
        ) as sample:
            with patch.object(
                Quiz, "display", autospec=True,
                side_effect=lambda quiz: displayed.append(quiz),
            ):
                with redirect_stdout(io.StringIO()):
                    result = self.game.play_quizzes(reader)

        sample.assert_called_once_with(original, 2)
        self.assertEqual(displayed, selected)
        self.assertEqual(result, 2)
        self.assertEqual(reader.call_args_list[0].args[1:], (1, 4))
        self.assertEqual(reader.call_count, 3)
        self.assertEqual(self.game.quizzes, original)

    def test_real_selection_has_no_duplicates(self):
        """실제 무작위 선택에서 개수·중복·원본 유지를 확인한다."""
        for count in (1, 2, 4):
            with self.subTest(count=count):
                original = list(self.game.quizzes)
                displayed = []
                reader = unittest.mock.Mock(
                    side_effect=[count] + [1] * count
                )

                with patch.object(
                    Quiz, "display", autospec=True,
                    side_effect=lambda quiz: displayed.append(quiz),
                ):
                    with redirect_stdout(io.StringIO()):
                        result = self.game.play_quizzes(reader)

                self.assertEqual(len(displayed), count)
                self.assertEqual(len({id(q) for q in displayed}), count)
                self.assertTrue(all(q in original for q in displayed))
                self.assertEqual(result, count)
                self.assertEqual(self.game.quizzes, original)

    def test_empty_list_does_not_request_input(self):
        """빈 목록에서는 문제 수 입력과 무작위 선택을 하지 않는다."""
        self.game.quizzes = []
        reader = unittest.mock.Mock()

        with patch("quiz_game.random.sample") as sample:
            with redirect_stdout(io.StringIO()) as output:
                result = self.game.play_quizzes(reader)

        self.assertIsNone(result)
        reader.assert_not_called()
        sample.assert_not_called()
        self.assertIn("등록된 퀴즈가 없습니다.", output.getvalue())

    def test_count_validation_retries(self):
        """문제 수의 문자·빈 입력·범위 오류 후 정상 입력을 받는다."""
        original = list(self.game.quizzes)

        with patch(
            "builtins.input",
            side_effect=["abc", "", "0", "5", "2", "1", "1"],
        ):
            with redirect_stdout(io.StringIO()) as output:
                result = self.game.play_quizzes(read_int)

        text = output.getvalue()
        self.assertIn("숫자로 입력해 주세요.", text)
        self.assertIn("입력이 비어 있습니다.", text)
        self.assertIn("1~4 사이의 번호를 입력해 주세요.", text)
        self.assertEqual(result, 2)
        self.assertEqual(self.game.quizzes, original)


if __name__ == "__main__":
    unittest.main()