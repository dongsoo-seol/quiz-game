# 1단계. 환경과 저장소 준비

## 수행 목표

Python 실행 환경과 Git을 확인하고, 미션 2 전용 저장소의 첫 업로드를 완료한다.

## 학습 목표

- Git의 필요성을 설명한다.
- init, add, commit, push의 역할을 구분한다.
- 로컬 저장소와 원격 저장소를 구분한다.

## 실행 환경

| 항목 | 확인 결과 |
|---|---|
| 운영체제 | Windows 10 Pro |
| 쉘 | Windows PowerShell |
| Python | 3.12.10 |
| Git | 2.56.0.windows.4 |
| 프로젝트 위치 | C:\Users\user\quiz-game |

## Python 설치와 확인

처음에는 py 명령을 찾지 못했고, python --version에서도 버전 번호가 나오지 않았다.

명령이 연결된 위치를 확인했다.

```powershell
where.exe python
```

```text
C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe
```

다음 명령으로 Python을 설치하고 설치 성공을 확인했다.

```powershell
winget install --id Python.Python.3.12 -e
```

새 PowerShell 창에서 버전과 실행을 확인했다.

```powershell
python --version
```

```text
Python 3.12.10
```

```powershell
python -c "print('Python 실행 성공')"
```

```text
Python 실행 성공
```

Python 3.10 이상이라는 과제 조건을 만족한다.

## Git 확인

```powershell
git --version
```

```text
git version 2.56.0.windows.4
```

## 프로젝트 폴더 준비

기존 폴더가 없는지 확인한 뒤 생성했다.
확인한 작업 위치: C:/Users/user/quiz-game

## 초기 파일 준비

- .gitignore 작성 및 내용 확인
- README.md 작성 및 오타 수정
- 환경 확인 문서 작성

## 진행 상태

- [x] Python 설치 및 실행 확인
- [x] Git 버전 확인
- [x] 프로젝트 폴더 준비
- [x] .gitignore 작성
- [x] 초기 README 작성
- [x] 환경 확인 문서 작성
- [ ] Git 저장소 초기화
- [ ] 첫 커밋
- [ ] GitHub 연결 및 첫 푸시
- [ ] 환경 스크린샷 저장

미완료 항목은 실제 수행 후 기록한다.
