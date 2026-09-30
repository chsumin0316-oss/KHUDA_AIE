from sqlalchemy.orm import Session
from modles import Game, Candidate, Tries


def get_game_by_id(session: Session, game_id: int) -> Game | None:
    return session.get(Game, game_id)


def get_answer_word(session: Session, game_id: int) -> str | None:
    game = session.get(Game, game_id)
    if game is None:
        return None
    candidate = session.get(Candidate, game.answer_id)
    return candidate.word if candidate else None


def get_tries(session: Session, game_id: int, user_id: int) -> list[Tries]:
    return (
        session.query(Tries)
        .filter(Tries.game_id == game_id, Tries.user_id == user_id)
        .order_by(Tries.attempt_num)
        .all()
    )


def create_try(
    session: Session,
    game_id: int,
    user_id: int,
    attempt_num: int,
    guess_word: str,
    result: str,
    is_solved: bool,
) -> Tries:
    new_try = Tries(
        game_id=game_id,
        user_id=user_id,
        attempt_num=attempt_num,
        guess_word=guess_word,
        result=result,
        is_solved=is_solved,
    )
    session.add(new_try)
    session.commit()
    session.refresh(new_try)
    return new_try