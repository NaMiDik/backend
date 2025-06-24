from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime, DECIMAL, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    categories = relationship("Category", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('income', 'expense', 'saving', name='category_types'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    transaction_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    amount_limit = Column(DECIMAL(10, 2), nullable=False)
    month = Column(String(7), nullable=False)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
