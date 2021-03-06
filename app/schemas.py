from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

     
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
  
    
class PostCreate(PostBase):
    pass

#schema for the response
class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
  
        
#base model for user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
#user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
class TokenData(BaseModel):
    id: Optional[str] = None