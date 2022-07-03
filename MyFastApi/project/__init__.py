from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .common import create_access_token
from .database import database as connection
from .database import User, Movie, UserReview
from .routers import user_router, review_router

app =   FastAPI(title='Proyecto para Peliculas',
                description='En este proyecto seremos capaces de reseñar peliculas',
                version='1')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)

@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    if user:
        return {
            "access_token": create_access_token(user),
            "token_type": 'Bearer'
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Username o Password Incorrectos',
        headers={'WWW-Authenticate': 'Beraer'})


app.include_router(api_v1)

#Evento 1
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    #se crean tablas, si estas existen no pasa nada.
    connection.create_tables([User, Movie, UserReview])
       
#Evento 2
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
