from fastapi import FastAPI,APIRouter
from . import schemas,models,database
from .routers import user,book,auth

app = FastAPI()

router = APIRouter()

models.Base.metadata.create_all(bind = database.engine)

app.include_router(user.router)
app.include_router(book.router)
app.include_router(auth.router)
@app.get('/')
def homepage():
    return {'welcome user':{'Hi!'}}