from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


# приймає email та сеанс бази даних db та повертає
# об'єкт користувача з бази даних, якщо він існує з такою адресою електронної пошти
async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves the user using its email value
    :param email: user email 
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: returns the user from the database.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


#  Створює нового користувача у базі даних, а потім повертає щойно створений об'єкт User.
async def create_user(body: UserModel, db: Session) -> User:
    """
    Creating a new user using the User model

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
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
    """
    Update user refresh token

    :param user: The user to update refresh token for .
    :type user: User
    :param token: refresh token to upgrade to 
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()


# встановити атрибут confirmed користувача в значення True у базі даних.
async def confirmed_email(email: str, db: Session) -> None:
    """
    Sets the value of the email as confirmed

    :param email: user email 
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Updates the user's avatar using cloudinary

    :param email: user email 
    :type email: str
    :param url: cloudinary url 
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: updated user avatar.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user