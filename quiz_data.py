from quiz import Quiz


def create_default_quizzes():
    quiz_data = [
        {
            "question": "카페의 한 달 매출이 2,000만 원이고, 같은 달의 전체 비용이 1,600만 원이라면 이익은 얼마인가요?",
            "choices": ["800만 원", "600만 원", "400만 원", "1,200만 원"],
            "answer": 3,
        },
        {
            "question": "월 임대료가 정액으로 정해진 카페에서, 판매량이 변해도 매월 일정하게 발생하는 고정비는 무엇인가요?",
            "choices": [
                "판매한 음료에 사용한 원두 비용",
                "판매한 음료에 사용한 일회용 컵 비용",
                "월 임대료",
                "판매한 음료에 사용한 우유 비용",
            ],
            "answer": 3,
        },
        {
            "question": "음료 한 잔을 판매할 때마다 일회용 컵 비용이 200원씩 발생합니다. 음료 100잔에 사용한 컵 비용은 얼마인가요?",
            "choices": ["2,000원", "10,000원", "20,000원", "200,000원"],
            "answer": 3,
        },
        {
            "question": "카페의 한 달 매출과 같은 달의 전체 비용이 같아 이익이 0원이 되는 상태를 무엇이라고 하나요?",
            "choices": ["손익분기점", "매출 증가", "적자", "변동비 증가"],
            "answer": 1,
        },
        {
            "question": "두 지역의 카페 수 자료를 비교하기 전에 확인해야 할 사항으로 가장 적절한 것은 무엇인가요?",
            "choices": [
                "표의 글자 색만 확인한다.",
                "자료의 기준일, 출처, 지역 범위와 업종 분류를 확인한다.",
                "숫자가 큰 지역을 무조건 좋은 상권으로 판단한다.",
                "자료 제목만 보고 비교한다.",
            ],
            "answer": 2,
        },
    ]

    quizzes = []

    for data in quiz_data:
        quiz = Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )
        quizzes.append(quiz)

    return quizzes