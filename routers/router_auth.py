from fastapi import APIRouter, HTTPException, status, Depends
from classes import schemas_dto, database, models_orm
from sqlalchemy.orm import Session
import utilities

# Formulaire de lancement du OAuth /auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def auth_team(
        payload : OAuth2PasswordRequestForm= Depends(), 
        cursor: Session= Depends(database.get_cursor)
    ):
    print(payload.__dict__)
    # 1. Recup les crédentials (username car il provient du formulaire par default de FastAPI)
    corresponding_team = cursor.query(models_orm.Teams).filter(models_orm.Teams.teamid == payload.username).first()
    # 2. Vérifier dans la DB si user exist
    if(not corresponding_team):
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail='id not good'
         )
    # 3. Vérif sur passwork hashé
    valid_pwd = utilities.verify_password(
        payload.password,
        utilities.hash_password(payload.password)
     )
    if(not valid_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='password not good' 
        ) 
    # 4. Génération du JWT
    token = utilities.generate_token(corresponding_team.teamid)
    print(token)
    return token

