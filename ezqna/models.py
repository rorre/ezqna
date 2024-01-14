from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Boolean, ForeignKey, MetaData
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)

if TYPE_CHECKING:
    BaseModel = Base
else:
    BaseModel = db.Model


class User(BaseModel):
    __tablename__ = "users"

    # Flask-Login stuffs
    is_authenticated = True
    is_active = True
    is_anonymous = False

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    token: Mapped[str] = mapped_column(String)
    token_secret: Mapped[str] = mapped_column(String)
    avatar: Mapped[str] = mapped_column(String, default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    questions: Mapped[list["Question"]] = relationship(back_populates="user")

    def get_id(self):
        return self.username

    def to_token(self):
        return {
            "oauth_token": self.token,
            "oauth_token_secret": self.token_secret,
            "user_id": self.id,
            "screen_name": self.username,
        }


class Question(BaseModel):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped[User | None] = relationship(back_populates="questions")
