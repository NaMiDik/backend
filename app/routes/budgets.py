from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database, auth

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.get("/", response_model=list[schemas.Budget])
def read_budgets(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Budget).filter(models.Budget.user_id == current_user.id).all()


@router.post("/", response_model=schemas.Budget)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_budget = models.Budget(**budget.dict(), user_id=current_user.id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.put("/{budget_id}", response_model=schemas.Budget)
def update_budget(
    budget_id: int,
    updated_budget: schemas.BudgetCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    budget = db.query(models.Budget).filter_by(id=budget_id, user_id=current_user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    for key, value in updated_budget.dict().items():
        setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    budget = db.query(models.Budget).filter_by(id=budget_id, user_id=current_user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(budget)
    db.commit()
    return

