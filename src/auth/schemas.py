from pydantic import BaseModel, Field, UUID4


class LoginSchema(BaseModel):
    username: str = Field(..., max_length=155, min_length=2)
    password: str = Field(..., min_length=8)


class UserSchema(BaseModel):
    name: str = Field(..., max_length=255)
    username: str = Field(..., max_length=155)
    is_admin: bool = None
    
    
class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=255)
    username: str = Field(..., max_length=155)
    

class PasswordSchema(BaseModel):
    user_id: UUID4
    password: str