import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from quiz_data import create_default_quizzes


class TestConsole(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.root = Path(self.temporary_directory.name)
        source = Path(__file__).resolve().parent

        for name in ("main.py", "quiz.py", "quiz_data.py", "quiz_game.py"):
            shutil.copy2(source / name, self.root / name)

        self.state_path = self.root / "state.json"
        self.questions = [
            {
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
            }
            for quiz in create_default_quizzes()
        ]

    def write_state(self, quizzes=None, best_score=None):
        if quizzes is None:
            quizzes = self.questions

        data = {
            "quizzes": quizzes,
            "best_score": best_score,
        }
        self.state_path.write_text(
            json.dumps(data, ensure_ascii=False),
            encoding="utf-8",
        )

    def read_state(self):
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def run_program(self, inputs="", cwd=None, script=None):
        command = [sys.executable, "-X", "utf8"]

        if script is None:
            command.append(str(self.root / "main.py"))
        else:
            command.extend(["-c", script])

        result = subprocess.run(
            command,
            input=inputs,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd or self.root,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result.stdout

    def play_inputs(self, correct_count):
        answers = []

        for index, question in enumerate(self.questions):
            answer = question["answer"]

            if index >= correct_count:
                answer = answer % 4 + 1

            answers.append(str(answer))

        return "1\n" + "\n".join(answers) + "\n5\n"

    def test_first_run_without_file(self):
        output = self.run_program("5\n")

        self.assertIn("저장 파일이 없어 기본 퀴즈를 사용합니다.", output)
        data = self.read_state()
        self.assertGreaterEqual(len(data["quizzes"]), 5)
        self.assertIsNone(data["best_score"])

    def test_broken_json_recovers(self):
        self.state_path.write_text("{ broken json", encoding="utf-8")

        output = self.run_program("5\n")

        self.assertIn("기본 퀴즈와 미플레이 상태로 복구합니다.", output)
        data = self.read_state()
        self.assertEqual(data["quizzes"], self.questions)
        self.assertIsNone(data["best_score"])

    def test_invalid_state_recovers(self):
        self.state_path.write_text(
            '{"quizzes": "invalid", "best_score": -1}',
            encoding="utf-8",
        )

        output = self.run_program("5\n")

        self.assertIn("기본 퀴즈와 미플레이 상태로 복구합니다.", output)
        data = self.read_state()
        self.assertEqual(data["quizzes"], self.questions)
        self.assertIsNone(data["best_score"])

    def test_menu_input_validation(self):
        self.write_state()

        output = self.run_program("abc\n\n0\n9\n 3 \n5\n")

        self.assertIn("숫자로 입력해 주세요.", output)
        self.assertIn("입력이 비어 있습니다.", output)
        self.assertIn("1~5 사이의 번호를 입력해 주세요.", output)
        self.assertIn("등록된 퀴즈 목록:", output)
        self.assertIn("게임을 종료합니다.", output)

    def test_quiz_input_validation_and_full_score(self):
        self.write_state()

        first_answer = self.questions[0]["answer"]
        remaining = [
            str(question["answer"])
            for question in self.questions[1:]
        ]

        inputs = (
            "1\nabc\n\n0\n5\n"
            + f" {first_answer} \n"
            + "\n".join(remaining)
            + "\n4\n5\n"
        )
        output = self.run_program(inputs)
        total = len(self.questions)

        self.assertIn("숫자로 입력해 주세요.", output)
        self.assertIn("입력이 비어 있습니다.", output)
        self.assertIn("1~4 사이의 번호를 입력해 주세요.", output)
        self.assertIn(
            f"결과: {total}문제 중 {total}문제 정답!",
            output,
        )
        self.assertEqual(self.read_state()["best_score"], total)

    def test_first_zero_score_and_restart(self):
        self.write_state()

        before = self.run_program("4\n5\n")
        self.assertIn("아직 완료한 퀴즈 기록이 없습니다.", before)

        output = self.run_program(self.play_inputs(0))
        self.assertIn("새로운 최고 점수를 저장했습니다!", output)
        self.assertEqual(self.read_state()["best_score"], 0)

        restarted = self.run_program("4\n5\n")
        self.assertIn("최고 점수: 0개 정답", restarted)
        self.assertNotIn("아직 완료한 퀴즈 기록이 없습니다.", restarted)

    def test_best_score_lower_equal_and_higher(self):
        self.write_state(best_score=2)

        for correct_count in (0, 2):
            with self.subTest(correct_count=correct_count):
                output = self.run_program(
                    self.play_inputs(correct_count)
                )
                self.assertIn("기존 최고 점수를 유지했습니다.", output)
                self.assertEqual(self.read_state()["best_score"], 2)

        total = len(self.questions)
        output = self.run_program(self.play_inputs(total))

        self.assertIn("새로운 최고 점수를 저장했습니다!", output)
        self.assertEqual(self.read_state()["best_score"], total)

        restarted = self.run_program("4\n5\n")
        self.assertIn(f"최고 점수: {total}개 정답", restarted)

    def test_add_list_restart_and_play_added_quiz(self):
        self.write_state()

        output = self.run_program(
            "2\n종합 검증 문제\n보기1\n보기2\n보기3\n보기4\n1\n3\n5\n"
        )

        self.assertIn("퀴즈를 추가하고 파일에 저장했습니다.", output)
        self.assertIn("종합 검증 문제", output)

        data = self.read_state()
        self.assertEqual(len(data["quizzes"]), len(self.questions) + 1)
        self.assertEqual(data["quizzes"][-1]["answer"], 1)
        self.assertIsNone(data["best_score"])

        answers = [
            str(question["answer"])
            for question in self.questions
        ]
        answers.append("1")

        restarted = self.run_program(
            "1\n" + "\n".join(answers) + "\n4\n5\n"
        )
        total = len(answers)

        self.assertIn('종합 검증 문제', restarted)
        self.assertIn(
            f"결과: {total}문제 중 {total}문제 정답!",
            restarted,
        )
        self.assertEqual(self.read_state()["best_score"], total)

    def test_empty_quizzes(self):
        self.write_state(quizzes=[])

        output = self.run_program("3\n1\n4\n5\n")

        self.assertGreaterEqual(
            output.count("등록된 퀴즈가 없습니다."),
            2,
        )
        self.assertIn("아직 완료한 퀴즈 기록이 없습니다.", output)
        self.assertEqual(self.read_state()["quizzes"], [])
        self.assertIsNone(self.read_state()["best_score"])

    def test_eof_keeps_completed_score(self):
        first_answer = self.questions[0]["answer"]

        cases = [
            "",
            "1\n",
            f"1\n{first_answer}\n",
            "2\n",
            "2\n미완성 문제\n보기1\n",
        ]

        for inputs in cases:
            with self.subTest(inputs=inputs):
                self.write_state(best_score=2)
                output = self.run_program(inputs)

                self.assertIn(
                    "입력이 종료되어 게임을 안전하게 종료합니다.",
                    output,
                )
                data = self.read_state()
                self.assertEqual(data["quizzes"], self.questions)
                self.assertEqual(data["best_score"], 2)

    def test_keyboard_interrupt_handler(self):
        cases = [
            ["<STOP>"],
            ["1", "<STOP>"],
            ["2", "미완성 문제", "보기1", "<STOP>"],
        ]

        for values in cases:
            with self.subTest(values=values):
                self.write_state(best_score=2)

                script = (
                    "import builtins,runpy\n"
                    f"values=iter({values!r})\n"
                    "def fake_input(prompt):\n"
                    "    value=next(values)\n"
                    "    if value == '<STOP>':\n"
                    "        raise KeyboardInterrupt\n"
                    "    return value\n"
                    "builtins.input=fake_input\n"
                    "runpy.run_path('main.py',run_name='__main__')\n"
                )

                output = self.run_program(script=script)

                self.assertIn(
                    "입력이 취소되어 게임을 안전하게 종료합니다.",
                    output,
                )
                data = self.read_state()
                self.assertEqual(data["quizzes"], self.questions)
                self.assertEqual(data["best_score"], 2)

    def test_save_failure_on_exit(self):
        self.state_path.mkdir()

        output = self.run_program("5\n")

        self.assertIn("저장 자료를 불러오지 못했습니다:", output)
        self.assertIn("데이터를 저장하지 못했습니다:", output)
        self.assertIn("종료 시 저장하지 못했습니다.", output)
        self.assertTrue(self.state_path.is_dir())

    def test_run_from_another_directory(self):
        self.write_state()
        other_directory = self.root / "another-directory"
        other_directory.mkdir()

        output = self.run_program("4\n5\n", cwd=other_directory)

        self.assertIn("아직 완료한 퀴즈 기록이 없습니다.", output)
        self.assertTrue(self.state_path.is_file())
        self.assertFalse((other_directory / "state.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)