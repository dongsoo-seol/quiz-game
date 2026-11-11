def show_menu():
    print("\n=== 나의 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def main():
    running = True

    while running:
        show_menu()
        choice = input("선택: ")

        if choice == "1":
            print("퀴즈 풀기는 다음 단계에서 구현합니다.")
        elif choice == "2":
            print("퀴즈 추가는 다음 단계에서 구현합니다.")
        elif choice == "3":
            print("퀴즈 목록은 다음 단계에서 구현합니다.")
        elif choice == "4":
            print("점수 확인은 다음 단계에서 구현합니다.")
        elif choice == "5":
            print("게임을 종료합니다.")
            running = False
        else:
            print("1~5 중에서 선택해 주세요.")


if __name__ == "__main__":
    main()