from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto


router = APIRouter(
    prefix = '/teams',
    tags=['Teams']
)

# Read
@router.get('')
async def get_all_teams(cursor: Session = Depends(get_cursor)):
    all_teams = cursor.query(models_orm.Teams).all()
    return all_teams


# Read by id
@router.get("/{teamid}", response_model=schemas_dto.Team_GETID_Response)
async def get_team(teamid: int, cursor: Session= Depends(get_cursor)):
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == teamid).first()
    if (corresponding_team):
        return corresponding_team
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding team found with id : {teamid}"
        )
    
# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_team(payload :schemas_dto.Team_POST_Body, cursor:Session= Depends(get_cursor)):
    new_team = models_orm.Teams(teamid = payload.teamid, teamname = payload.teamname, league = payload.league, marketvalue = payload.marketvalue)
    cursor.add(new_team)
    cursor.commit()
    cursor.refresh(new_team)
    return {"message" : f"New team {new_team.teamname} added sucessfully with id : {new_team.teamid}"}


# DELETE
@router.delete('/{teamid}', status_code=status.HTTP_204_NO_CONTENT)
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
    

# Update
@router.patch('/{teamid}')
async def update_team(teamid: int,payload:schemas_dto.Team_UPDATE_Body, cursor: Session= Depends(get_cursor)):
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == teamid)
    if (corresponding_team.first()):
        corresponding_team.update({'marketvalue':payload.newmarketvalue})
        cursor.commit()
        return corresponding_team.first()
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'New market value add for team : {teamid}'
        )