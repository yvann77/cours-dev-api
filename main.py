from fastapi import FastAPI,Body,Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

# Description
api_description = description = """
Football API help you to find players and teams.

## Players
You will be able to : 
* Create New Players
* Get Players by id
"""
# Liste des tags utilises dans la doc

tags_metadata = [{
    "name" : "Players",
    "description" : " Manage Players. So _Fancy_ they have their own docs",
    "externalDocs" : {
        "description" : "Items external docs",
        "url":"https://fastapi.taingolo.com/",
    }
    },
]

# APP
app = FastAPI(
    title="Football API",
    description= api_description,
    openapi_tags= tags_metadata # Tags metadata
)



class Player (BaseModel):
        playerid: int
        player_name: str
        team: str
        position: str
        image: str
        imageavailable: bool = True
        listetransfer: Optional [str]
        
playerslist = [ {
        "playerid": 1,
        "player_name": "Hector Bellerin",
        "team": "Betis",
        "position": "Defender",
        "image": "hectorbellerin.jpg"
        },
        {
            "playerid": 2,
            "player_name": "Olivier Giroud",
            "team": "AC Milan",
            "position": "Striker",
            "image": "oliviergiroud.jpg"
        }]

@app.get("/")
async def root():
    return {"message": "sheshhhhh"}

@app.get("/players/", tags=["Players"])
async def get_Players():
    return {
        "players" : playerslist,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }


@app.post("/players/",tags=["Players"])
async def create_player(payload: Player, response:Response):
    print(payload.last_name)
    playerslist.append(payload.dict())

    response.status_code = status.HTTP_201_CREATED
    return {"message" :f"Un Nouveau joueur a été ajouté : {payload.player_name}"}


@app.get("/players/{playerid}",tags=["Players"])
async def get_player(playerid: int, response:Response): 
     try:
        corresponding_player = playerslist[playerid - 1]
        return corresponding_player
     except:
        raise HTTPException(status_code=404, detail="Player not found")
     

# DELETE 
@app.delete("/players/{playerid}",tags=["Players"])
async def delete_player(playerid:int, response:Response):
    try:
        playerslist.pop(playerid - 1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "Player not found"
        )


# PUT (Update, remplacer)
@app.put("/players/{playerid}" ,tags=["Players"])
async def replace_player(playerid : int, payload:Player, response:Response) : 
    try:
        playerslist[playerid - 1] = payload.dict()
        return {"message" : f"Player updated successfully : {payload.player_name}"}
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail= "Player not found")
    

# USERS 
class User (BaseModel):
        userid: int
        user_name: str
        position: str
        
userslist = [ {
        "userid": 1,
        "user_name": "Yvann Yvann Gaucho",
        "position": "Ailier Gauche",
        },
        {
            "userid": 2,
            "user_name": "Alexis Renidola",
            "position": "Milieu défensif",
        }]

@app.get("/users/",tags=["Users"])
async def get_Users():
    return {
        "users" : userslist,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }


@app.post("/users/", tags=["Users"])
async def create_user(payload: User, response:Response):
    print(payload.user_name)
    userslist.append(payload.dict())

    response.status_code = status.HTTP_201_CREATED
    return {"message" :f"Un Nouveau user a été ajouté : {payload.user_name}"}

@app.get("/users/{userid}", tags=["Users"])
async def get_user(userid: int, response:Response): 
     try:
        corresponding_user = userslist[userid - 1]
        return corresponding_user
     except:
        raise HTTPException(status_code=404, detail="User not found")
     
# DELETE 
@app.delete("/users/{userid}", tags=["Users"])
async def delete_user(userid:int, response:Response):
    try:
        userslist.pop(userid - 1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    

# PUT(Update, remplacer)
@app.put("/users/{userid}", tags=["Users"])
async def replace_user(userid : int, payload:User, response:Response) : 
    try:
        userslist[userid - 1] = payload.dict()
        return {"message" : f"Player updated successfully : {payload.user_name}"}
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail= "Player not found")
    



# TEAMS
class Team (BaseModel):
        teamid: int
        teamname: str
        league: str
        country : str
        championsleague : bool
        chapeau: int

teamslist = [{
        "teamid": 1,
        "teamname": "Barcelona",
        "league": "La Liga",
        "country" : "Espagne",
        "championsleague" : True,
        "chapeau" : 1
        },
        {
            "teamid": 2,
            "teamname": "Arsenal",
            "league": "Premier League",
            "country" : "Angleterre",
            "championsleague" : True,
            "chapeau" : 2
        }]

@app.get("/teams/", tags=["Teams"])
async def get_Teams():
    return {
        "users" : teamslist,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }
@app.post("/teams/", tags=["Teams"])
async def create_team(payload: Team, response:Response):
    print(payload.teamname)
    teamslist.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    return {"message" :f"Une Nouvelle équipe a été ajouté : {payload.teamname}"}



@app.get("/teams/{teamid}", tags=["Teams"])
async def get_team(teamid: int, response:Response): 
     try:
        corresponding_team = teamslist[teamid - 1]
        return corresponding_team
     except:
        raise HTTPException(status_code=404, detail="Team not found")

# DELETE 
@app.delete("/teams/{teamid}", tags=["Teams"])
async def delete_team(teamid:int, response:Response):
    try:
        teamslist.pop(teamid - 1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "Team not found"
        )
    

# PUT (Update, remplacer)
@app.put("/teams/{teamid}", tags=["Teams"])
async def replace_team(teamid : int, payload:Team, response:Response) : 
    try:
        teamslist[teamid - 1] = payload.dict()
        return {"message" : f"Team updated successfully : {payload.teamname}"}
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail= "Team not found")
    