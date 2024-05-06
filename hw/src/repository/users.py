from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

# приймає email та сеанс бази даних db та повертає 
# об'єкт користувача з бази даних, якщо він існує з такою адресою електронної пошти
async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

#  Створює нового користувача у базі даних, а потім повертає щойно створений об'єкт User.
async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# оновлює поле refresh_token користувача та фіксує зміни у базі даних.
async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
