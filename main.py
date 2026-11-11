from quiz_game import QuizGame


def show_menu():
    print("\n=== 나의 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def read_int(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()

        if not text:
            print("입력이 비어 있습니다. 번호를 입력해 주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자로 입력해 주세요.")
            continue

        if number < minimum or number > maximum:
            print(f"{minimum}~{maximum} 사이의 번호를 입력해 주세요.")
            continue

        return number


def main():
    game = QuizGame()
    running = True

    try:
        while running:
            show_menu()
            choice = read_int("선택: ", 1, 5)

            if choice == 1:
                correct_count = game.play_quizzes(read_int)

                if correct_count is not None:
                    game.update_best_score(correct_count)

            elif choice == 2:
                game.add_quiz(read_int)

            elif choice == 3:
                game.show_quiz_list()

            elif choice == 4:
                game.show_best_score()

            elif choice == 5:
                print("게임을 종료합니다.")
                running = False

    finally:
        if not game.save_state():
            print("종료 시 저장하지 못했습니다. 저장 오류를 확인해 주세요.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n입력이 취소되어 게임을 안전하게 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 게임을 안전하게 종료합니다.")