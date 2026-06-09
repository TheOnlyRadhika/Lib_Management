from pydantic import BaseModel
from pydantic import EmailStr

class CreateBook(BaseModel):
    name : str
    author : str
    isbn: str
    category: str
    no_of_copies : int
    available_copies: int

class CreateMember(BaseModel):
    name :str
    email :EmailStr
    phone_number : str

class BorrowBook(BaseModel):
    member_id : int
    book_id: int



