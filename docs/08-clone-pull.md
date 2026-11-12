# 8단계. 저장소 복제와 변경사항 가져오기

## 1. 수행 목표

GitHub 저장소를 별도 폴더에 복제하고, 복제 폴더에서 올린 변경을 원래 작업 폴더로 가져온다.

## 2. 학습 목표

- clone과 pull의 차이를 설명한다.
- 로컬 저장소와 원격 저장소의 관계를 이해한다.
- 서로 다른 작업 폴더 사이에서 GitHub를 통해 변경사항을 전달한다.

## 3. 사용한 저장소와 폴더

- GitHub: https://github.com/dongsoo-seol/quiz-game
- 원래 작업 폴더: C:\Users\user\quiz-game
- 복제 작업 폴더: C:\Users\user\quiz-game-copy
- 사용 브랜치: main

## 4. 저장소 복제

복제할 폴더가 없는지 확인했다.

```powershell
Test-Path "$HOME\quiz-game-copy"
```

결과:

```text
False
```

사용자 폴더로 이동한 뒤 저장소를 복제했다.

```powershell
cd "$HOME"
git clone https://github.com/dongsoo-seol/quiz-game.git quiz-game-copy
```

복제 결과에서 다음 내용을 확인했다.

```text
Receiving objects: 100% (128/128)
Resolving deltas: 100% (66/66)
```

clone은 원격 저장소의 파일과 변경 이력을 새로운 로컬 폴더에 복제하는 명령이다.

## 5. 복제 폴더의 작성자 설정

복제 폴더로 이동하여 작업 상태를 확인했다.

```powershell
cd "$HOME\quiz-game-copy"
git status
```

main 브랜치이며 작업 폴더에 변경사항이 없었다.

복제 저장소의 커밋 작성자 설정이 없어 user.name과 user.email을 해당 저장소에 설정했다.

설정 후 다음 결과를 확인했다.

```text
커밋 작성자 설정 확인 완료
```

이 문서에는 작성자의 이메일 값을 기록하지 않는다.

## 6. 복제 폴더에서 수정·커밋·업로드

README에 다음 실습 기록을 추가했다.

```text
## 저장소 복제 실습

- GitHub 저장소를 quiz-game-copy 폴더에 clone하고, 복제한 저장소에서 README 수정 실습을 진행했습니다.
```

변경 내용을 확인한 뒤 커밋하고 업로드했다.

```powershell
git add README.md
git commit -m "Docs: 복제 저장소에서 README 수정 실습 기록"
git push origin main
```

결과:

```text
커밋: beaa8ff
메시지: Docs: 복제 저장소에서 README 수정 실습 기록
업로드: 3d4a288..beaa8ff  main -> main
```

## 7. 원래 폴더에서 pull

원래 작업 폴더로 이동했다.

```powershell
cd "$HOME\quiz-game"
git status
```

작업 폴더에 변경사항이 없음을 확인한 뒤 실행했다.

```powershell
git pull --ff-only origin main
```

실제 결과:

```text
Updating 3d4a288..beaa8ff
Fast-forward
README.md | 5 ++++-
1 file changed, 4 insertions(+), 1 deletion(-)
```

pull은 기존 로컬 저장소에 원격 저장소의 변경사항을 가져와 반영하는 명령이다.

--ff-only는 별도 병합 커밋 없이 현재 브랜치를 앞으로 이동할 수 있는 경우에만 반영하도록 제한한다.

## 8. 반영 결과 확인

```powershell
git --no-pager log -1 --oneline
```

결과:

```text
beaa8ff (HEAD -> main, origin/main) Docs: 복제 저장소에서 README 수정 실습 기록
```

README 마지막 부분도 확인했다.

```powershell
Get-Content -Encoding UTF8 .\README.md -Tail 6
```

복제 폴더에서 추가한 저장소 복제 실습 내용이 원래 폴더에도 표시되었다.

## 9. clone과 pull의 차이

| 명령 | 사용하는 상황 | 이번 실습 |
|---|---|---|
| clone | 저장소를 새 폴더에 처음 복제할 때 | quiz-game-copy 생성 |
| pull | 이미 있는 저장소에 원격 변경을 반영할 때 | 원래 quiz-game 폴더 갱신 |

## 10. 진행 상태

- [x] 별도 폴더에 clone
- [x] 복제 폴더의 커밋 작성자 설정
- [x] 복제 폴더에서 README 수정
- [x] 복제 폴더에서 commit과 push
- [x] 원래 폴더에서 pull
- [x] 최신 커밋과 README 반영 확인
- [x] README의 8단계 진행 상태 갱신
- [ ] 8단계 수행 문서 GitHub 업로드
- [ ] 최종 제출 자료 확인