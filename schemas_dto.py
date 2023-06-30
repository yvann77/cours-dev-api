from typing import Optional
from pydantic import BaseModel
# DTO : DATA TRANSFERT OBJECT

class Team_POST_Body (BaseModel):
        teamid: int
        teamname: str
        league: str
        country : str
        championleague : bool
        chapeau: int
class Team_UPDATE_Body (BaseModel):
        newteamid: int