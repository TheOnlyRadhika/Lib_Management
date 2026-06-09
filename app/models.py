from  sqlalchemy import Column, Date , Integer , String
from app.database import Base
# from pydantic import EmailStr
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True)
    name = Column(String , nullable = False)
    author = Column(String , nullable = False)
    isbn = Column(String , unique = True)
    category = Column(String)
    no_of_copies = Column(Integer)
    available_copies = Column(Integer)

    borrow_records = relationship("BorrowRecord", back_populates = "book")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    email = Column(String, unique = True)
    phone_number = Column(String , unique = True)

    borrow_records = relationship("BorrowRecord",back_populates="member")


class BorrowRecord(Base):
    __tablename__ = "borrow_records"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer,ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    
    member = relationship("Member", back_populates="borrow_records")
    book = relationship("Book", back_populates= "borrow_records")
