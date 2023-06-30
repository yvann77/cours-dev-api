from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_cursor
import models_orm, schemas_dto
router = APIRouter(
    prefix = '/teams'
)



@router.get("/teams/")
async def get_Teams(cursor: Session= Depends(get_cursor)):
    print(cursor.query(models_orm.Teams))
    all_teams = cursor.query(models_orm.Teams).all() # Lancement de la requete
    return {
        "teams" : all_teams,
        "limit": 10,
        "total": 2,
        "skip": 0,
    }

@router.get("/teams/{teamid}")
async def get_team_by_id(teamid: int, cursor: Session= Depends(get_cursor)):
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == teamid).first()
    if (corresponding_team):
        return corresponding_team
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding team found with id : {teamid}"
        )
    

@router.post('/teams', status_code=status.HTTP_201_CREATED)
async def create_team(payload :schemas_dto.Team_POST_Body, cursor:Session= Depends(get_cursor)):
    new_team = models_orm.Teams(teamid = payload.teamid, teamname = payload.teamname, league = payload.league ,country = payload.country, championleague = payload.championleague, chapeau = payload.chapeau)
    cursor.add(new_team)
    cursor.commit()
    cursor.refresh(new_team)
    return {"message" : f"New team {new_team.teamname} added sucessfully with id : {new_team.teamid}"}


@router.delete('/teams/{teamid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(teamid: int, cursor: Session= Depends(get_cursor)):
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == teamid)
    if (corresponding_team.first()):
        corresponding_team.delete()
        cursor.commit()
        return
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding team found with id : {teamid}"
        )
    


@router.patch('/teams/{teamid}')
async def update_team(teamid: int,payload:schemas_dto.Team_UPDATE_Body, cursor: Session= Depends(get_cursor)):
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == teamid)
    if (corresponding_team.first()):
        corresponding_team.update({'featured':payload.newteamid})
        cursor.commit()
        return corresponding_team.first()
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding team found with id : {teamid}'
        )