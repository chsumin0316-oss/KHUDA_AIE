from pydantic import BaseModel, Field
from fastapi import FastAPI

from database.db_connection import engine
from database.orm import Base
import modles
from service import user_word as process_user_word, get_current_answer

Base.metadata.create_all(bind=engine)
app = FastAPI()


class UserRequest(BaseModel):
    user: str = Field(min_length=7, max_length=7)
    attempt: int = Field(ge=1, le=6)
    game_id: int
    user_id: int



@app.post("/user")
def user_word(request: UserRequest):
    return process_user_word(request.user.upper(), request.attempt, request.game_id, request.user_id)


@app.get("/answer")
def get_answer(game_id: int):
    return {
        "정답": get_current_answer(game_id)
    }