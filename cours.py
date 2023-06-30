from fastapi import FastAPI,Body,Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

# Connexion DB
connexion = psycopg2.connect(
    host="dpg-ci8rn35gkuvmfnsaactg-a.frankfurt-postgres.render.com",
    database = "football_render",
    user="yvann_render",
    password="IDpYil4X9K3VWiF1oyzAXwB1cFQj8pvp",
    cursor_factory=RealDictCursor
)
cursor = connexion.cursor() 

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

@app.get("/")
async def root():
    return {"message": "sheshhhhh"}

# TEAMS
class Team (BaseModel):
        teamid: int
        teamname: str
        league: str
        country : str
        championleague : bool
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
    # REQUETE SQL
    cursor.execute("SELECT * FROM team")
    dbTeams= cursor.fetchall()
    return {
        "users" : dbTeams,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }


@app.post("/teams/", tags=["Teams"])
async def create_team(payload: Team, response:Response):
    print(payload.teamname)
    cursor.execute("INSERT INTO team (teamname,league,country,championleague,chapeau) VALUES (%s,%s,%s,%s,%s) RETURNING *;",(payload.teamname,payload.league,payload.country,payload.championleague,payload.chapeau))
    connexion.commit() # Sauvagarder dans la base de données
    response.status_code = status.HTTP_201_CREATED
    return {"message" :f"Une Nouvelle équipe a été ajouté : {payload.teamname}"}



@app.get("/teams/{teamid}", tags=["Teams"])
async def get_team(teamid: int, response:Response): 
     try:
        cursor.execute(f"SELECT * FROM team WHERE teamid={teamid}")
        corresponding_team = cursor.fetchone()
        if(corresponding_team):
            return corresponding_team
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail= "Team not found"
            )
     except:
        raise HTTPException(status_code=404, detail="Team not found")

# DELETE 
@app.delete("/teams/{teamid}", tags=["Teams"])
async def delete_team(teamid:int, response:Response):
        cursor.execute(
            "DELETE FROM team where teamid=%s RETURNING *;",
            (teamid,)
        )
        connexion.commit()
        return {"message" : f"Team deleted"}

    

@app.put("/teams/{teamid}", tags=["Teams"])
async def replace_team(teamid: int, payload: Team, response: Response):
    try:
        cursor.execute(
            'UPDATE team SET teamid = %s, teamname = %s, league = %s, country = %s, chapeau = %s WHERE teamid = %s RETURNING *;',
            (payload.teamid, payload.teamname, payload.league, payload.country, payload.chapeau, teamid),
        )
        connexion.commit()
        return {"message": f"Team updated successfully: {payload.teamname}"}
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")