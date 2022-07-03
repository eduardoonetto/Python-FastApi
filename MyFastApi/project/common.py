from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .database import User

SECRET_KEY = 'CCF202219746549'

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')

def create_access_token(user, seconds=3600):
    data = {
        'user_id': user.id,
        'username':user.username,
        'exp': datetime.utcnow() + timedelta(seconds=seconds)
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return None

def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)
    if data:
        print('midata', data)
        return User.select().where(User.id == data['user_id']).first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Access-Token invalid',
        headers={'WWW-Authenticate': 'Beraer'})