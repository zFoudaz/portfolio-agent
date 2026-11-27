from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from github_ai_agent.core.app import send_message_streamed
from github_ai_agent.backend import schemas
from github_ai_agent.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# CORS
origins = settings.origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get('/health')
def health_check(request:Request):
    return {'state':'healthy'}

@app.post('/send_message',response_class=StreamingResponse)
@limiter.limit('10/hour')
def send_message(request:Request, message_request:schemas.MessageRequest):
    thread_id = message_request.thread_id
    message = message_request.message
    return StreamingResponse(send_message_streamed(thread_id,message))

