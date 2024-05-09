from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from datetime import datetime
from src.database.models import User
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


# отримати список контактів
@router.get('/', response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.
    
    :param skip: Skip a number of records
    :type skip: int
    :param limit: Limit the number of contacts returned
    :type limit: int
    :param db: Pass the database session to the function
    :type db: Session
    :param current_user: Get the user from the database
    :type current_user: User
    :return: A list of contacts
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get('/find_birthday', response_model=List[ContactResponse])
async def contacts_birthday(db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The contacts_birthday function returns a list of contacts with upcoming birthdays.
    
    :param skip: Skip the first n contacts in the database
    :type skip: int
    :param limit: Limit the number of contacts returned
    :type limit: int
    :param db: Get a database session
    :type db: Session
    :param current_user: Get the current user from the database
    :type current_user: User
    :return: A list of contacts
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts_birthday(current_user, db)
    return contacts

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(skip: int = 0,
                        limit: int = 100,
                        first_name: str = Query(None),
                        last_name:  str = Query(None),
                        email:  str = Query(None),
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_contacts function allows you to search for contacts in the database.
    
    :param skip: Skip the first n records
    :type skip: int
    :param limit: Limit the number of results returned
    :type limit: int
    :param first_name: Filter the contacts by firstname
    :type first_name: str
    :param last_name: Filter the contacts by lastname
    :type last_name: str
    :param email: Filter the contacts by email
    :type email: str
    :param db: Pass the database connection to the function
    :type db: Session
    :param current_user: Get the user that is currently logged in
    :type current_user: User
    :return: A list of contacts, 
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.search_contacts(
        skip, limit, first_name, last_name, email,current_user, db)
    
    return contacts

# отримати один контакт за ідентифікатором
@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), 
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to retrieve a single contact from the database.
    
    :param contact_id: Specify the contact id to be read
    :type ontact_id: int
    :param db: Pass the database session to the function
    :type db: Session
    :param current_user: Get the user information from the token
    :type current_user: User
    :return: A contact object
    :rtype: ContactResponse
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# створення контакту
@router.post('/', response_model=ContactResponse)
async def create_contact(body:ContactModel, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
 
    :param body: Get the data from the request body
    :type body: ContactModel
    :param db: Pass the database session to the function
    :type db: Session
    :param current_user: Get the user information from the token
    :type current_user: User
    :return: A contactmodel object
    :rtype: ContactResponse
    """
    return await repository_contacts.create_contact(body, current_user,db)

# оновити існуючий контакт
@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body:ContactModel, contact_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    
    :param body: Get the data from the request body
    :type body: ContactModel
    :param contact_id: Identify the contact that is to be deleted
    :type contact_id: int
    :param db: Pass the database session to the function
    :type db: Session
    :param current_user: Get the user information from the token
    :type current_user: User
    :return: The updated contact
    :rtype: ContactResponse
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# видалити контакт
@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
    
    :param contact_id: Specify the contact to be deleted
    :type contact_id: int
    :param db: Pass the database session to the function
    :type db: Session
    :param current_user: Get the user information from the token
    :type current_user: User
    :return: A contact object
    :rtype: ContactResponse
    """
    contact = await repository_contacts.delete_contact(contact_id, current_user,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

