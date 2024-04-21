from typing import List

from sqlalchemy.orm import Session
from datetime import datetime
from src.database.models import Contact
from src.schemas import ContactModel

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone_number=body.phone_number, birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:   
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(contact_id:int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contact_fname(fname :str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.first_name == fname).all()

async def get_contact_lname(lname :str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.last_name == lname).all()

async def get_contact_email(email :str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.email == email).all()

async def get_contacts_birthday(db: Session)-> List[Contact]:
    contacts = []
    now = datetime.now()
    for contact in db.query(Contact).all():
        date_cont = datetime(year=now.year, month=contact.birthday.month, day=contact.birthday.day)
        d = date_cont - now 
        if d.days <= 7 and d.days >= -1:
            contacts.append(contact)
        
    return contacts


    

async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number= body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id:int, db: Session) -> Contact| None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

