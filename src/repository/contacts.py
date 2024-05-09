from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.models import Contact, User
from src.schemas import ContactModel
from sqlalchemy import and_

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creating a contact for a registered user using the contact model

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(firstname=body.firstname, lastname=body.lastname, 
                      email=body.email, phone_number=body.phone_number, birthday=body.birthday, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(contact_id:int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """

    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

async def search_contacts(skip: int,
                       limit: int,
                       firstname: str | None,
                       lastname: str | None,
                       email: str | None,
                       user: User,
                       db: Session) -> List[Contact]:
    """
    Retrieves contacts that match the search parameters for a specific user

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param firstname: contact firstname.
    :type firstname: str | None
    :param lastname: contact lastname.
    :type lastname : str | None
    :param email: contact email.
    :type email: str | None
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    filters = []
    if firstname:
        filters.append(Contact.firstname == firstname)
    if lastname:
        filters.append(Contact.lastname == lastname)
    if email:
        filters.append(Contact.email == email)

    if not filters:
        raise HTTPException(status_code=400, detail="Search criteria are not specified")

    return db.query(Contact).filter(*filters, Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contacts_birthday(user: User, db: Session)-> List[Contact]:
    """
    Receives contacts who will have birthdays this week

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    contacts = []
    now = datetime.now()
    for contact in db.query(Contact).filter(Contact.user_id == user.id).all():
        date_cont = datetime(year=now.year, month=contact.birthday.month, day=contact.birthday.day)
        d = date_cont - now 
        if d.days <= 7 and d.days >= -1:
            contacts.append(contact)
        
    return contacts


async def update_contact(contact_id: int, body: ContactModel, user: User , db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone_number= body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id:int, user: User, db: Session) -> Contact| None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Сontact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

