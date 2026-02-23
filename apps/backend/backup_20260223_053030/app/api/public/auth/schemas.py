from pydantic import BaseModel, EmailStr, Field, validator

class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Full name of the citizen")
    email: EmailStr = Field(..., description="Email address")
    nif: str = Field(..., min_length=9, max_length=14, description="National Identity Number (NIF)")
    password: str = Field(..., min_length=8, description="Password")

    @validator('nif')
    def validate_nif(cls, v):
        # Basic format validation can be added here
        if not v.isalnum():
            raise ValueError('NIF must correspond to valid format')
        return v.upper()
