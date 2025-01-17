from db.db import db
from db.models import EducationalOrganization, Event, EducationalOrganizationEvent
from main import app


with app.app_context():
    db.session.query(
        EducationalOrganizationEvent
    ).delete() 
    db.session.commit()
    db.session.query(
        EducationalOrganization
    ).delete()  # Очистка таблицы EducationalOrganization
    db.session.query(Event).delete()  # Очистка таблицы Event
    db.session.commit()
    print("Таблицы очищены.")
