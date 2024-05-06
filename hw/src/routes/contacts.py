from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from datetime import datetime
from src.database.models import User
from src.services.auth import Auth as auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


# отримати список контактів
@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get('/find_birthday', response_model=List[ContactResponse])
async def contacts_birthday(db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
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
    contacts = await repository_contacts.search_contacts(
        skip, limit, first_name, last_name, email,current_user, db)
    
    return contacts

# отримати один контакт за ідентифікатором
@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), 
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# створення контакту
@router.post('/', response_model=ContactResponse)
async def create_contact(body:ContactModel, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user,db)

# оновити існуючий контакт
@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body:ContactModel, contact_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# видалити контакт
@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, current_user,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

