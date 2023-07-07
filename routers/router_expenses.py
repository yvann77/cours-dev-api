from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto
import utilities
from sqlalchemy.exc import IntegrityError

# Ajout du schema Oauth sur un endpoint précis (petit cadenas)
# Le boutton "Authorize" ouvre un formulaire en popup pour capturer les credentials
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/expenses',
    tags=['Expenses']
)


# Read Expenses
@router.get('')
async def list_expense_by_teamid(
    token: Annotated[str, Depends(oauth2_scheme)], 
    cursor: Session = Depends(get_cursor)):
        # Le décodage du token permet de récupérer l'identifiant du customer
        decoded_teamid = utilities.decode_token(token)
        all_expenses = cursor.query(models_orm.Expenses).filter(models_orm.Expenses.teamid == decoded_teamid).all()
        return all_expenses # data format à ajuster cela besoin


# CREATE NEW TEAM EXPENSES
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_team_expenses(payload :schemas_dto.Expenseteam_POST_Body, cursor:Session= Depends(get_cursor)):
    new_teamexpenses = models_orm.Expenses(expensesid = payload.expensesid,teamid = payload.teamid, arrivalsnumber = payload.arrivalsnumber, teamexpenses = payload.teamexpenses, revenues = payload.revenues, balance = payload.revenues, teamname = payload.teamname)
    cursor.add(new_teamexpenses)
    cursor.commit()
    cursor.refresh(new_teamexpenses)
    return {"message" : f"New team {new_teamexpenses.teamname} added sucessfully with id : {new_teamexpenses.expensesid}"}

