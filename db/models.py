from db.db import db


class EducationalOrganization(db.Model):
    __tablename__ = "educational_organization"
    id = db.Column(db.Integer, primary_key=True)
    club_members_grade1 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade2 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade3 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade4 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade5 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade6 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade7 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade8 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade9 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade10 = db.Column(db.Integer, default=0, nullable=False)
    club_members_grade11 = db.Column(db.Integer, default=0, nullable=False)
    students_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    sports = db.relationship(
        "Sport",
        secondary="educational_organization_sport",
        back_populates="organizations",
    )
    events = db.relationship(
        "Event",
        secondary="educational_organization_event",
        back_populates="organizations",
    )


class EducationalOrganizationEvent(db.Model):
    __tablename__ = "educational_organization_event"
    educational_organization_id = db.Column(
        db.Integer, db.ForeignKey("educational_organization.id"), primary_key=True
    )
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), primary_key=True)


class EducationalOrganizationSport(db.Model):
    __tablename__ = "educational_organization_sport"
    educational_organization_id = db.Column(
        db.Integer, db.ForeignKey("educational_organization.id"), primary_key=True
    )
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), primary_key=True)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    organizations = db.relationship(
        "EducationalOrganization",
        secondary="educational_organization_event",
        back_populates="events",
    )


class Sport(db.Model):
    __tablename__ = "sport"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    organizations = db.relationship(
        "EducationalOrganization",
        secondary="educational_organization_sport",
        back_populates="sports",
    )
