import json
from pathlib import Path

from quiz import Quiz
from quiz_data import create_default_quizzes


class QuizGame:
    def __init__(self):
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.use_default_state()
        self.load_state()

    def use_default_state(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def load_state(self):
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 자료는 딕셔너리 형태여야 합니다.")

            quiz_data = data["quizzes"]
            best_score = data["best_score"]

            if not isinstance(quiz_data, list):
                raise ValueError("퀴즈 목록은 리스트여야 합니다.")

            if best_score is not None:
                if type(best_score) is not int or best_score < 0:
                    raise ValueError("최고 점수는 0 이상의 정수여야 합니다.")

            loaded_quizzes = []

            for item in quiz_data:
                if not isinstance(item, dict):
                    raise ValueError("각 퀴즈는 딕셔너리 형태여야 합니다.")

                quiz = Quiz(
                    question=item["question"],
                    choices=item["choices"],
                    answer=item["answer"],
                )
                loaded_quizzes.append(quiz)

            self.quizzes = loaded_quizzes
            self.best_score = best_score

        except FileNotFoundError:
            self.use_default_state()
            print("저장 파일이 없어 기본 퀴즈를 사용합니다.")
            return False

        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            self.use_default_state()
            print(f"저장 자료를 불러오지 못했습니다: {error}")
            print("기본 퀴즈와 미플레이 상태로 복구합니다.")
            return False

        print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개")
        return True

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
        }

        temporary_path = self.state_path.with_name(
            self.state_path.name + ".tmp"
        )

        try:
            text = json.dumps(
                data,
                ensure_ascii=False,
                indent=4,
                allow_nan=False,
            )

            with temporary_path.open("w", encoding="utf-8") as file:
                file.write(text)

            temporary_path.replace(self.state_path)

        except (OSError, UnicodeError, TypeError, ValueError) as error:
            print(f"데이터를 저장하지 못했습니다: {error}")
            return False

        return True

    def play_quizzes(self, read_number):
            if not self.quizzes:
                print("등록된 퀴즈가 없습니다.")
                return None

            correct_count = 0
            total = len(self.quizzes)

            print(f"\n퀴즈를 시작합니다. 총 {total}문제입니다.")

            for number, quiz in enumerate(self.quizzes, start=1):
                print(f"\n[문제 {number}/{total}]")
                quiz.display()

                answer = read_number("정답 번호(1~4): ", 1, 4)

                if quiz.check_answer(answer):
                    print("정답입니다!")
                    correct_count += 1
                else:
                    print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            print(f"\n결과: {total}문제 중 {correct_count}문제 정답!")
            return correct_count

    def show_best_score(self):
        if self.best_score is None:
            print("아직 완료한 퀴즈 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}개 정답")


    def update_best_score(self, correct_count):
        if type(correct_count) is not int or correct_count < 0:
            raise ValueError("정답 수는 0 이상의 정수여야 합니다.")

        is_new_record = (
            self.best_score is None
            or correct_count > self.best_score
        )

        if is_new_record:
            self.best_score = correct_count

        if not self.save_state():
            print("점수는 메모리에 유지되지만 이번 파일 저장은 실패했습니다.")
            return False

        if is_new_record:
            print("새로운 최고 점수를 저장했습니다!")
        else:
            print("기존 최고 점수를 유지했습니다.")

        self.show_best_score()
        return True

    def read_nonempty_text(self, prompt):
        while True:
            text = input(prompt).strip()

            if not text:
                print("내용이 비어 있습니다. 다시 입력해 주세요.")
                continue

            return text


    def add_quiz(self, read_number):
        print("\n새로운 퀴즈를 추가합니다.")

        question = self.read_nonempty_text("문제: ")
        choices = []

        for number in range(1, 5):
            choice = self.read_nonempty_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = read_number("정답 번호(1~4): ", 1, 4)

        quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
        )

        self.quizzes.append(quiz)

        if not self.save_state():
            self.quizzes.pop()
            print("저장에 실패해 새 문제 등록을 취소했습니다.")
            return False

        print("퀴즈를 추가하고 파일에 저장했습니다.")
        print(f"등록된 퀴즈: {len(self.quizzes)}개")
        return True

    def show_quiz_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return 0

        total = len(self.quizzes)
        print(f"\n등록된 퀴즈 목록: 총 {total}개")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

        return total
