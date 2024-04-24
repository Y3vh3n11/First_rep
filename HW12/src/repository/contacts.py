from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.models import Contact, User
from src.schemas import ContactModel
from sqlalchemy import and_


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        user=user,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


async def search_contacts(
    skip: int,
    limit: int,
    first_name: str | None,
    last_name: str | None,
    email: str | None,
    user: User,
    db: Session,
) -> List[Contact]:
    filters = []
    if first_name:
        filters.append(Contact.first_name == first_name)
    if last_name:
        filters.append(Contact.last_name == last_name)
    if email:
        filters.append(Contact.email == email)

    if not filters:
        raise HTTPException(status_code=400, detail="Search criteria are not specified")

    return (
        db.query(Contact)
        .filter(*filters, Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contacts_birthday(user: User, db: Session) -> List[Contact]:
    contacts = []
    now = datetime.now()
    for contact in db.query(Contact).filter(Contact.user_id == user.id).all():
        date_cont = datetime(
            year=now.year, month=contact.birthday.month, day=contact.birthday.day
        )
        d = date_cont - now
        if d.days <= 7 and d.days >= -1:
            contacts.append(contact)

    return contacts


async def update_contact(
    contact_id: int, body: ContactModel, user: User, db: Session
) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact
