from fastapi import FastAPI
from database import database as connection
from database import User, Movie, UserReview
from schemas import UserBaseModel

app =   FastAPI(title='Proyecto para Peliculas',
                description='En este proyecto seremos capaces de reseñar peliculas',
                version='1')

#Evento
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    #se crean tablas, si estas existen no pasa nada.
    connection.create_tables([User, Movie, UserReview])
       
#Evento
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()

#Disponibilzar Endpoints
@app.get('/')
async def index():
    return 'Hola Mundo desde un servidor en FastAPI.'

@app.get('/')
async def about():
    return 'About.'

@app.post('/users/')
async def create_user(user: UserBaseModel):
    user = User.create(
        username = user.username,
        password = user.password
    )

    return user.id