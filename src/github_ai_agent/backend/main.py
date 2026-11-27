from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from github_ai_agent.core.app import send_message_streamed
from github_ai_agent.backend import schemas

app = FastAPI()

@app.get('/healt')
def health_check():
    return {'state':'healthy'}

@app.post('/send_message',response_class=StreamingResponse)
def send_message(request:schemas.MessageRequest):
    thread_id = request.thread_id
    message = request.message
    return StreamingResponse(send_message_streamed(thread_id,message))

