from pydantic import BaseModel


class Team(BaseModel):
    id: str
    name: str
    flag_code: str = ""


class Group(BaseModel):
    name: str
    teams: list[Team]
