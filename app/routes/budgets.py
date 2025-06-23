from fastapi import APIRouter
router = APIRouter(prefix='/budgets')

@router.get('/')
def read_budgets():
    return {'msg': 'Budgets route'}
