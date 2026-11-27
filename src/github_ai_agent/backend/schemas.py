from pydantic import BaseModel

class MessageRequest(BaseModel):
    thread_id:str 
    message:str