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

    while running:
        show_menu()
        choice = read_int("선택: ", 1, 5)

        if choice == 1:
            game.play_quizzes(read_int)
        elif choice == 2:
            print("퀴즈 추가는 다음 단계에서 구현합니다.")
        elif choice == 3:
            print("퀴즈 목록은 다음 단계에서 구현합니다.")
        elif choice == 4:
            print("점수 확인은 다음 작업에서 구현합니다.")
        elif choice == 5:
            print("게임을 종료합니다.")
            running = False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n입력이 취소되어 게임을 안전하게 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 게임을 안전하게 종료합니다.")