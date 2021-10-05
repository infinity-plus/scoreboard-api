from datetime import date as dt
from typing import Optional

from pydantic import EmailStr
from tortoise import fields
from tortoise.fields.relational import ForeignKeyRelation
from tortoise.models import Model


class Score(Model):
    id: int = fields.IntField(pk=True)
    score: int = fields.IntField(default=0)
    date: dt = fields.DateField(default=dt.today)
    team: ForeignKeyRelation["Team"] = fields.ForeignKeyField(
        "models.Team", related_name="scores"
    )


class Team(Model):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=20, index=True)
    scores: fields.ReverseRelation["Score"]

    def __str__(self):
        return f"{self.name}"


class User(Model):
    id: int = fields.IntField(pk=True)
    username: str = fields.CharField(max_length=20, index=True)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str

    def __str__(self):
        return f"{self.username}"
