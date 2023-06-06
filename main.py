from fastapi import FastAPI,Body
app = FastAPI() #nom de variable
from pydantic import BaseModel
from typing import Optional

class Player (BaseModel):
        identifier: int
        first_name: str
        last_name: str
        team: str
        position: str
        image: str
        imageavailable: bool = True
        listetransfer: Optional [str]
        
playerslist = [ {
        "identifier": 1003,
        "first_name": "Hector",
        "last_name": "Bellerin",
        "team": "Betis",
        "position": "Defender",
        "image": "hectorbellerin.jpg"
        },
        {
            "identifier": 1402,
            "first_name": "Olivier",
            "last_name": "Giroud",
            "team": "AC Milan",
            "position": "Striker",
            "image": "oliviergiroud.jpg"
        }]

@app.get("/")
async def root():
    return {"message": "sheshhhhh"}

@app.get("/players/")
async def getPlayers():
    return {
        "players" : playerslist,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }


@app.post("/players/")
async def create_post(payload: Player):
    print(payload.last_name)
    playerslist.append(payload.dict())
    return {"message" :f"Un Nouveau joueur a été ajouté : {payload.last_name}"}