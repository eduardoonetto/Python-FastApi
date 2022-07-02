from timeit import repeat
from pydantic import BaseModel, ValidationError, validator
from typing import Optional

class User(BaseModel):
    username    : str #Requerido
    password    : str #Requerido
    repeat_pass : str #Requerido
    email       : str #Requerido
    age         : Optional[int] = None #Opcional

    @validator('username')
    def username_validation_lenght(cls, username):
        if(len(username) < 3):
            raise ValueError('Logitud Minima es de 4 Caracteres')
        
        if(len(username) > 50):
            raise ValueError('Logitud maxima es de 50 Caracteres')

        return username

    @validator('repeat_pass')
    def repeat_pass_validation(cls, repeat_pass, values):
        if 'password' in values and repeat_pass != values['password']:
            raise ValueError('Las Password no coinciden.')

        return repeat_pass

try:
    user1 = User(
        username = 'Eduardo',
        password = 'Pass123',
        repeat_pass = 'Pass1234',
        email    = 'eduardo.onetto@email.com',
        age      = 23
    )

    print(user1)
except ValidationError as e:
    print(e.json)