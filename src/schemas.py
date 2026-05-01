import re
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class UserCreate(BaseModel):
    username: str = Field(min_length=4, max_length=20, pattern="^[a-zA-Z0-9]+$")
    
    email: EmailStr
    
    password: str
    confirm_password: str
    
    age: int = Field(ge=18, le=100)

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.search(r'[A-Z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        
        if not re.search(r'[!@#$%^&*]', value):
            raise ValueError('Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*)')
            
        return value

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError('Пароли не совпадают')
        return self