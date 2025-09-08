from fastapi import APIRouter,Depends,HTTPException
from .. import schemas,database,models
from sqlalchemy.orm import Session 
from ..hashing import Hash


router = APIRouter(tags=['User'], prefix="/user")

@router.post('/',response_model=schemas.showUser)
async def create_user(request: schemas.Usercreate, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt(request.password)

    new_user = models.User(
        username = request.username,
        email=request.email,
        password=hashed_password,
        bio=request.bio
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemas.showUser)
async def getbyid(id:int , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail='User not found')
    return user