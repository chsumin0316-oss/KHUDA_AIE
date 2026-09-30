from repository import get_answer_word, create_try
from sqlalchemy.orm import Session

def check_word(user: str, answer: str) -> list[str]:
    result = []
    user = user.upper()
    answer = answer.upper()

    for i in range(len(answer)):
        if user[i] == answer[i]:
            result.append("correct")
        elif user[i] in answer:
            result.append("wrong_position")
        else:
            result.append("not_in_word")

    return result


def user_word(user: str, attempt: int, game_id: int, user_id: int, session: Session) -> dict:
    answer = get_answer_word(session, game_id)
    if answer is None:
        return {"error": "게임 데이터가 없습니다. candidate/game 테이블에 데이터를 넣어주세요."}

    result = check_word(user, answer)
    a = len(result) == len(answer) and all(x == "correct" for x in result)

    create_try(
        session,
        game_id=game_id,
        user_id=user_id,
        attempt_num=attempt,
        guess_word=user.upper(),
        result=",".join(result),
        is_solved=a,
    )

    if a:
        return {
            "success": "정답을 맞췄습니다!"
            }
    else:
        if attempt == 6:
            return {
                    "error": "6번의 시도 안에 정답을 맞추지 못했습니다."
            }
        else:
            return {
                "user": user,
                "attempt": attempt,
                "result": result
            }


def get_current_answer(game_id: int, session:Session) -> str | None:
        return get_answer_word(session, game_id)