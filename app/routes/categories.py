from fastapi import APIRouter
router = APIRouter(prefix='/categories')

@router.get('/')
def read_categories():
    return {'msg': 'Categories route'}
