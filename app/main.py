from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.database import Base , engine
from app.database import get_db 
from app.models import Book , Member , BorrowRecord
from app.schemas import CreateBook , CreateMember , BorrowBook
from fastapi import HTTPException
from datetime import date, timedelta

Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return{"message" : "Library hello API"}

@app.get("/books/search")
def search_book(title: str , db : Session = Depends(get_db)):
    books = db.query(Book).filter(Book.name.contains(title)).all()
    return books


@app.post("/books")
def create_book(book: CreateBook, db: Session = Depends(get_db)):
   
   New_book = Book(
        name=book.name,
        author=book.author,
        isbn=book.isbn,
        category=book.category,
        no_of_copies=book.no_of_copies,
        available_copies=book.available_copies
    )
   db.add(New_book)
   db.commit()
   return {"message": "Book added successfully"}

@app.get("/books/{book_id}")
def get_books(book_id = int ,db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id ).first(),
    if book is None:
       raise HTTPException(
        status_code=404,
        detail="Book not found"
    )
    return book

@app.put("books/{book_id}")
def update_book(book_id = int , updated_book = CreateBook , db : Session = Depends (get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code = 404,
            details = "Book not present ",
        )
    
    book.name =updated_book.name,
    book.author = updated_book.author,
    book.isbn = updated_book.isbn,
    book.category = updated_book.category,
    book.no_of_copies = updated_book.no_of_copies,
    book.available_copies = updated_book.available_copies

   
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
    ):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)

    db.commit()

    return {
        "message": "Book deleted successfully"
    }




@app.post("/members")
def create_member(member: CreateMember , db: Session = Depends(get_db)):
    new_mem = Member(
        name =  member.name,
        email = member.email,
        phone_number = member.phone_number,
    )

    db.add(new_mem)
    db.commit()
    return {"message": "Member added successfully"}

@app.get("/members/{member_id}")
def get_member(member_id: int , db: Session= Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    return member

@app.put("members/{member_id}")
def update_member(member_id = int , updated_member = CreateMember , db: Session = Depends (get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(
            status_code = 404,
            details = "Member not present ",
        )
    
    member.name = updated_member.name,
    member.email = updated_member.email,
    member.phone_number = updated_member.phone_number

   
    db.commit()
    db.refresh(member)
    return member

@app.delete("/members/{member_id}")
def delete_member(member_id : int, db: Session= Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(
            status_code = 404,
            message = "Member not found",
        )
    db.delete(member)
    db.commit()
    db.refresh(member)
    return {"message" : "Member deleted successfully"}


@app.post("/borrow_records")
def create_record(request : BorrowBook, db : Session = Depends(get_db)):

    mem_id = db.query(Member).filter(Member.id == request.member_id).first()
    if mem_id is None:
        raise HTTPException(
            status_code = 404,
            detail = "Member not found"
        )
    book_id = db.query(Book).filter(Book.id == request.book_id).first()
    if book_id is None:
        raise HTTPException(
            status_code = 404,
            detail = "Book not found"
        )
    
    if book_id.available_copies <1:
        raise HTTPException(
            status_code = 404,
            detail = "Book not available"
        )
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=7)
    
    record = BorrowRecord(
        member_id = request.member_id,
        book_id = request.book_id,
        borrow_date = borrow_date,
        due_date = due_date,
        return_date=None
    )

    book_id.available_copies -= 1
    db.add(record)

    db.commit()
    db.refresh(record)
    return {"record_id" : record.id,
            "book_id" : record.book_id ,
            "member_id" : record.member_id ,
            "borrow_date" : record.borrow_date , 
            "due_date" : record.due_date}


@app.post("/return/{record_id}")
def update_record(record_id : int, db: Session= Depends(get_db)):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    
    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )
    
    if record.return_date is not None:
        raise HTTPException(
            status_code = 404,
            message = "Book Already returned",
        )
    member = db.query(Member).filter(Member.id == record.member_id).first()
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    book = db.query(Book).filter(Book.id == record.book_id).first()
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    record.return_date = date.today()
    
    book.available_copies += 1

    db.commit()
    db.refresh(record)
    return {"message" : "Returned Book successfully",
            "record_id": record.id,
            "book_id": record.book_id,
            "member_id": record.member_id,
            "return_date": record.return_date
        }


@app.get("/borrow_records")
def get_borrow_records(db: Session = Depends(get_db)):
    data = db.query(BorrowRecord).all(),
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="No borrow records found"
        )
    return data

@app.get("/currently_borrowed")
def get_curr_borrowed_books(db: Session = Depends(get_db)):
    data = db.query(BorrowRecord).filter(BorrowRecord.return_date == None).all(),
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="No currently borrowed books found"
        )
    return data
    

@app.get("/overdue_books")
def get_overdue_books(db: Session = Depends(get_db)):
    today = date.today()
    data = db.query(BorrowRecord).filter(BorrowRecord.due_date < today, BorrowRecord.return_date == None).all()
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="No overdue books found"
        )
    return data

@app.get("/test")
def test(db: Session = Depends(get_db)):

    record = db.query(BorrowRecord).first()

    return {
        "book_name": record.book.name,
        "member_name": record.member.name
    }