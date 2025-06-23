from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database, auth

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=list[schemas.Transaction])
def get_user_transactions(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
