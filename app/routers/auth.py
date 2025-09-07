from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..hashing import Hash
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

router = APIRouter(prefix='/auth', tags=['Authentication'])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # find user by email (stored in request.username)
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with email {request.username} not found"
        )

    # check password
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    # create access token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
