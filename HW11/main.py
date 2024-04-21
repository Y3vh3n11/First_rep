from fastapi import FastAPI

from src.routes import contacts

app = FastAPI()
# include_router - для включення маршрутизації,
# prefix використовується для зазначення загального префікса URL для всіх маршрутів цього модуля.
app.include_router(contacts.router, prefix='/api')


# маршрут за замовченням для маршруту
@app.get("/")
def read_root():
    return {"message": "Hello World"}

