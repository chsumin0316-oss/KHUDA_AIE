from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.orm import Base


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


class Candidate(Base):
    __tablename__ = "candidate"

    candidate_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    word: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_answer: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )


class Game(Base):
    __tablename__ = "game"

    game_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    game_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    answer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("candidate.candidate_id", ondelete="CASCADE"),
        nullable=False,
    )


class Tries(Base):
    __tablename__ = "tries"

    tries_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("game.game_id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    attempt_num: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    guess_word: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_solved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    __table_args__ = (
        UniqueConstraint("game_id", "user_id", "attempt_num", name="uq_tries_game_user_attempt"),
    )