from fastapi import FastAPI
import uvicorn

from src.routes import contacts, auth

app = FastAPI()
# include_router - для включення маршрутизації,
# prefix використовується для зазначення загального префікса URL для всіх маршрутів цього модуля.
app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

# маршрут за замовченням для маршруту
@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)