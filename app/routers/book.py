from fastapi import APIRouter,Depends,HTTPException
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session 
from ..hashing import Hash


router = APIRouter(tags=['Books'],prefix='/books')

@router.post('/',response_model=schemas.Book)
async def createbook(request:schemas.BookCreate,db: Session = Depends(database.get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    new_book = models.Books(
        name = request.name,
        type = request.type,
        owner_id= current_user.id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get('/{id}',response_model=schemas.Book)
async def get_book(id:int,db : Session = Depends(database.get_db)):
    curr_book = db.query(models.Books).filter(models.Books.id==id).first()
    if not curr_book:
        raise HTTPException(status_code=404,detail=f'book with {id} not found')
    return curr_book

@router.put('/update/{id}',response_model=schemas.BookCreate)
async def updatebook(id:int,request:schemas.BookCreate,db : Session = Depends(database.get_db)):
    curr_book = db.query(models.Books).filter(models.Books.id==id).first()
    if not curr_book:
        raise HTTPException(status_code=404,detail=f'book with {id} not found')
    else:
        curr_book.name = request.name
        curr_book.type = request.type

        db.commit()
        db.refresh(curr_book)
        return curr_book
    

@router.delete('/delete/{id}')
async def delete_book(id:int , db: Session = Depends(database.get_db)):
    book = db.query(models.Books).filter(models.Books.id==id).first()
    if not book:
        raise HTTPException(status_code=404,detail=f'book with {id} not found')
    
    db.delete(book)
    db.commit()
    return f'book of {id} is deleted '