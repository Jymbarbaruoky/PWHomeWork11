from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactResponse, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def querys_contacts(firstname: str, lastname: str, email: str, db: Session) -> List[Contact]:
    contact_with_firstname = db.query(Contact).filter(Contact.firstname == firstname).all()
    contact_with_lastname = db.query(Contact).filter(Contact.lastname == lastname).all()
    contact_with_email = db.query(Contact).filter(Contact.email == email).all()
    result = []
    result.extend(contact_with_firstname)
    result.extend(contact_with_lastname)
    result.extend(contact_with_email)
    return result


async def birthdays(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()
    result = []
    delta = timedelta(days=7)
    delta_date = datetime.now() + delta
    for contact in contacts:
        birthday_date = datetime(year=datetime.now().year, month=contact.birthday.month, day=contact.birthday.day)
        birthday_date_next_year = datetime(year=datetime.now().year + 1, month=contact.birthday.month, day=contact.birthday.day)
        if datetime.now() < birthday_date <= delta_date or datetime.now() < birthday_date_next_year <= delta_date:
            result.append(contact)
    return result
