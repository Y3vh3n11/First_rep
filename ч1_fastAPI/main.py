import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.routes import contacts, auth
from src.conf.config import settings

app = FastAPI()
origins = [ 
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    # визначає список джерел, яким дозволено доступ до застосунку.
    allow_origins=origins,
    # встановлює значення True, що означає, що дозволені кросдоменні запити з урахуванням облікових даних.
    allow_credentials=True,
    # визначає список дозволених методів HTTP,
    allow_methods=["*"],
    #визначає список дозволених заголовків HTTP, які можуть використовуватися в кросдоменних запитах. 
    allow_headers=["*"],
)

# include_router - для включення маршрутизації,
# prefix використовується для зазначення загального префікса URL для всіх маршрутів цього модуля.
app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

# маршрут за замовченням для маршруту
@app.get("/")
def read_root():
    return {"message": "Hello World"}
    
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)