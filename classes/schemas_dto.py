from pydantic import BaseModel
from datetime import datetime
# DTO : DATA TRANSFERT OBJECT
# Représente la structure de la données (data type) en entrée ou en sortie de la Football API.

# BODY FOR POST PER TEAM 
class Team_POST_Body (BaseModel):
        teamid: int
        teamname: str
        league: str
        marketvalue : str

# NEW MARKET VALUE UPTADED PER TEAM
class Team_UPDATE_Body (BaseModel):
        newmarketvalue: str

class Team_GETID_Response (BaseModel):
        teamid: int
        teamname: str
        league: str
        marketvalue : str
        class Config: # La Config ORM nous permet de "choisir" les columnes à montrer.
                orm_mode= True 

# BODY FOR POST FOR NEW EXPENSES DATA FOR A NEW TEAM
class Expenseteam_POST_Body (BaseModel):
        expensesid: int
        teamid: int
        arrivalsnumber: int
        teamexpenses : str
        revenues: str
        balance : str
        teamname : str


# BODY FOR POST FOR NEW EXPENSES DATA FOR A NEW TEAM
class transfer_POST_Body (BaseModel):
        transferid : int
        playername: str
        transferat: str
        age: int
        transferprice: str
 