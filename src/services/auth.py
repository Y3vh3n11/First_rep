import pickle
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import redis
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    # екземпляр класу OAuth2PasswordBearer, який забезпечує авторизацію по bearer токену
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    # перевіряє, чи відповідає простий текстовий пароль хешованому паролю.
    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. 

        :param self: Represent the instance of the class
        :param plain_password: Pass in the password that is entered by the user
        :param hashed_password: Check if the password is correct
        :return: True if the password is correct, and false otherwise
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    # хешує пароль за допомогою алгоритму bcrypt.
    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password and returns the hashed version of it.
      
        :param self: Represent the instance of the class
        :param password: Specify the password that will be hashed
        :type password: str
        :return: A hash of the password
        :rtype: str
        """
        return self.pwd_context.hash(password)
    # створює веб-токен JWT з областю дії scope, що дорівнює значенню access_token, 
    # який буде використовуватись для авторизації користувача для доступу до захищених ресурсів.
    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
       
        :param self: Refer to the current object
        :param data: Pass the data to be encoded in the jwt token
        :type data: dict
        :param expires_delta: the expiration time of the access token
        :type expires_delta: Optional[float]
        :return: A token that is encoded with the user's information,
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token
    
    # створює JWT з областю дії refresh_token, який можна використовувати для оновлення токена 
    # доступу access_token після закінчення терміну його дії.
    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
       
        :param self: Represent the instance of the class
        :param data: Pass the data that will be encoded into the token
        :type data: dict
        :param expires_delta: Set the expiration time of the refresh token
        :type expires_delta: Optional[float]
        :return: A string that contains the encoded refresh token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token
    
    # метод декодує токен оновлення refresh_token для отримання електронної пошти користувача.
    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function takes a refresh token and decodes it.

        :param self: Represent the instance of the class
        :param refresh_token: Pass in the refresh token that is sent to the server
        :type refresh_token: str
        :return: The email of the user who is trying to refresh their token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
   
   
    # авторизує користувача, розшифровуючи токен доступу access_token та, перевіряючи, чи існує користувач у базі даних.
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be called by FastAPI to
     
        :param self: Refer to the class itself
        :param token: Get the token from the request header
        :type token: str
        :param db:  Get the database session
        :type db: Session
        :return: The user object corresponding to the email in the jwt payload
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        
        user = self.r.get(f"user:{email}")
        # user = await repository_users.get_user_by_email(email, db)
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user
    

    # повертається закодований токен, що дійсний 7 днів
    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
            
        :param self: Make the function a method of the class
        :param data: Create a dictionary of the data that will be encoded into the token
        :type data: dict
        :return: A token that is encoded using the jwt library
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        If the token is invalid, it raises an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: Pass in the token that was sent to the user's email address
        :type token: str
        :return: The email address of the user if the token is valid
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()
