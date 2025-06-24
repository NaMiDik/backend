from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Transaction(BaseModel):
    id: int
    amount: float
    description: str
    transaction_date: date

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    category_id: Optional[int]
    amount: float
    description: Optional[str] = None
    transaction_date: date

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # замість orm_mode у Pydantic v2

class CategoryBase(BaseModel):
    name: str
    type: Literal['income', 'expense', 'saving'] # 'income' або 'expense'

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    category_id: int
    amount_limit: float
    month: str  # формат 'YYYY-MM'

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int
    category: Optional[Category]

    class Config:
        from_attributes = True