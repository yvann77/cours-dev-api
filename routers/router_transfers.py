from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto
import utilities
from sqlalchemy.exc import IntegrityError

# Ajout du schema Oauth sur un endpoint précis (petit cadenas)
# Le boutton "Authorize" ouvre un formulaire en popup pour capturer les credentials
from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/transfers',
    tags=['Transfers']
)

# Read Transfers by teamid with JWT AUTH and Limit and Offset query parameters
@router.get('')
async def list_transfers_by_teamid(
    token: Annotated[str, Depends(oauth2_scheme)], 
    cursor: Session = Depends(get_cursor),limit:int=10, offset:int=0):
        # Le décodage du token permet de récupérer l'identifiant du customer
        decoded_teamid = utilities.decode_token(token)
        all_transfers = cursor.query(models_orm.Transfers).filter(models_orm.Transfers.teamid == decoded_teamid).limit(limit).offset(offset).all()
        transfers_count = cursor.query(func.count(models_orm.Transfers.teamid)).scalar()
        return {
        "transfers" : all_transfers,
        "limit": limit,
        "total": transfers_count,
        "skip": offset
    }


# POST Transfers by teamid with JWT AUTH
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_transfer_by_teamid(
    token: Annotated[str, Depends(oauth2_scheme)], # Sécurisation par Auth 
    payload: schemas_dto.transfer_POST_Body,
    cursor: Session = Depends(get_cursor)
    ):
    decoded_teamid = utilities.decode_token(token)
    new_transfer= models_orm.Transfers(transferid=payload.transferid, playername=payload.playername, transferat=payload.transferat, age=payload.age, teamid=decoded_teamid, transferprice=payload.transferprice)
    try : 
        cursor.add(new_transfer)
        cursor.commit()
        cursor.refresh(new_transfer)
        return {'message' : f'New transfer of {new_transfer.playername} at {new_transfer.transferat} added in database' }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='The player have already been Transfered'
        )



