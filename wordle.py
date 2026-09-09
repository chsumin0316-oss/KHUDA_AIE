from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

answer = "FASTAPI"

#def modify_attempt():
 #   global attempt
 #   attempt = 0
 #전역변수로 쓰면 무상태 불가능, 서버가 횟수를 받아야함

class UserRequest(BaseModel):
    user: str = Field(min_length=7, max_length=7)
    attempt: int = Field(ge=1, le=6)

def check_word(user: str):
    result = []
    user = user.upper()

    for i in range(7):
        if user[i] == answer[i]:
            result.append("correct")
        elif user[i] in answer:
            result.append("wrong_position")
        else:
            result.append("not_in_word")

    return result

@app.post("/user")
def user_word(request: UserRequest):
    result = check_word(request.user.upper())
    a = len(result) == len(answer) and all(x == "correct" for x in result)

    if a:
        return {
            "success":"정답을 맞췄습니다!"
        }
    else:
        if request.attempt == 6:
            return {
                "error": "6번의 시도 안에 정답을 맞추지 못했습니다."
            }

        else:
            return {
                "user": request.user,
                "attempt": request.attempt,
                "result": result
            }

@app.get("/answer")
def get_answer():
    return {
        "정답": answer
    }

