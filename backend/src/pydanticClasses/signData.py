from pydantic import BaseModel, Field


class SignIn_request_pydantic (BaseModel):
    login: str = Field(min_length = 4)
    password: str = Field(min_length = 5)