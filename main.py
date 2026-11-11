from quiz_game import QuizGame


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
    game.run(read_int)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n입력이 취소되어 게임을 안전하게 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 게임을 안전하게 종료합니다.")