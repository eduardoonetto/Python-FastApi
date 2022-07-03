from ..schemas import ReviewResponseModel, UserRequestModel, UserResponseModel
from fastapi import APIRouter, HTTPException, Response, Cookie
from fastapi.security import HTTPBasicCredentials
from ..database import User
from typing import List

router= APIRouter(prefix='/users')

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El username ya esta en uso.')

    hash_password = User.create_password(user.password)

    user = User.create(
        username = user.username,
        password = hash_password
    )

    return user

@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username, User.create_password(credentials.password) == User.password).first()
   
    if user is None:
        raise HTTPException(404, 'Invalid Credentials')
    
    response.set_cookie(key='user_id', value=user.id)

    return user

@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(404, 'User not Found')
    
    return [user_review for user_review in user.reviews]
