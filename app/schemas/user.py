from pydantic import BaseModel

class user_create(BaseModel):
    name:str
    email:str
    password:str

class user_response(BaseModel):
    id:int
    name:str
    email:str
    role_id:int
    class config:
        from_attributes=True

class login_request(BaseModel):
    email:str
    password:str