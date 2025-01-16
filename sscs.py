import sys
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from db.db import db
from db.models import EducationalOrganization, Event, EducationalOrganizationEvent, EducationalOrganizationSport, Sport
from db.events import base_events, base_populate_event_table
from db.sports import base_populate_sport_table
from db.mapping import SPORT_MAPPING


# Configure logging
logging.basicConfig (
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("sscs.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
login = LoginManager(app)
app.secret_key = "your_secret_key"  # Key for sessions to store user data
login.login_view = "login"

# Temporary user store for demo purposes
# users = {"admin": {"password": "password"}}


# User class implementing UserMixin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id


@login.user_loader
def load_user(user_id):
    return User(user_id)
    # if user_id in users:
    #     return User(user_id)
    # return None


app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:sscsserverpostgres@sscsurvey.ru:5432/sscs_db?connect_timeout=10&sslmode=prefer"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def save_survey_data():
    block1_data = session.get("block1_data")
    block2_data = session.get("block2_data")
    block3_data = session.get("block3_data")
    school_name = session.get("school_name")

    if not block1_data:
        logging.warning("No Block 1 data found in session.")
        return

    # Ensure the organization exists
    organization = EducationalOrganization.query.filter_by(name=school_name).first()
    if not organization:
        organization = EducationalOrganization(
            students_number=block1_data["students_number"],
            club_members_grade1=block1_data["class1"],
            club_members_grade2=block1_data["class2"],
            club_members_grade3=block1_data["class3"],
            club_members_grade4=block1_data["class4"],
            club_members_grade5=block1_data["class5"],
            club_members_grade6=block1_data["class6"],
            club_members_grade7=block1_data["class7"],
            club_members_grade8=block1_data["class8"],
            club_members_grade9=block1_data["class9"],
            club_members_grade10=block1_data["class10"],
            club_members_grade11=block1_data["class11"],
            name=school_name,
        )
        db.session.add(organization)
        db.session.commit()
        logging.info(f"Created new EducationalOrganization: {school_name}")
    else:
        logging.info(f"Found existing EducationalOrganization: {school_name}")

    # Сохранение видов спорта и количества участников
    for sport_name, sport_id in SPORT_MAPPING.items():
        # Получаем название чекбокса и поля для численности
        checkbox_name = f"{sport_name}Check"
        count_name = f"{sport_name}Count"

        # Проверяем, выбран ли вид спорта
        if checkbox_name in block1_data and block1_data[checkbox_name]:
            # Извлекаем количество участников
            members = int(block1_data.get(count_name, 0))

            # Проверяем, есть ли уже запись в таблице
            org_sport = EducationalOrganizationSport.query.filter_by(
                educational_organization_id=organization.id, sport_id=sport_id
            ).first()

            if org_sport:
                # Обновляем численность
                org_sport.members = members
                logging.info(
                    f"Updated members for sport ID {sport_id} in organization {school_name} to {members}"
                )
            else:
                # Создаем новую запись
                org_sport = EducationalOrganizationSport(
                    educational_organization_id=organization.id,
                    sport_id=sport_id,
                    members=members,
                )
                db.session.add(org_sport)
                logging.info(
                    f"Added new sport ID {sport_id} with {members} members for organization {school_name}"
                )
    db.session.commit()

    # Save Block 2 data
    if block2_data:
        logging.info(f"Saving Block 2 events for: {school_name}")
        for event_data in block2_data.values():
            event = Event.query.filter_by(name=event_data["event_name"]).first()
            if not event:
                event = Event(name=event_data["event_name"])
                db.session.add(event)
                db.session.commit()
                logging.info(f"Created new Event: {event.name}")

            # Overwrite if differs
            edu_org_event = EducationalOrganizationEvent.query.filter_by(event_id=event.id, educational_organization_id=organization.id).first()
            if edu_org_event:
                if edu_org_event.participants != event_data["participants"] or edu_org_event.date_start.strftime("%Y-%m-%d") != event_data["date_start"] or edu_org_event.date_start.strftime("%Y-%m-%d") != event_data["date_end"]:
                    db.session.delete(edu_org_event)
                    db.session.commit()
                    logging.info(f"Overwriting existing relationship between Event({event.id}) and EducationalOrganization({organization.id})")
                    edu_org_event=None

            if not edu_org_event:
                edu_org_event = EducationalOrganizationEvent(
                    educational_organization_id=organization.id,
                    event_id=event.id,
                    participants=event_data["participants"],
                    date_start=event_data["date_start"],
                    date_end=event_data["date_end"],
                )
                db.session.add(edu_org_event)
        db.session.commit()

    # Save Block 3 data
    if block3_data:
        logging.info(f"Saving Block 3 events for: {school_name}")
        for event_info in block3_data.values():
            event = Event.query.filter_by(name=event_info["event_name"]).first()
            if not event:
                event = Event(name=event_info["event_name"])
                db.session.add(event)
                db.session.commit()
                logging.info(f"Created new Event: {event.name}")

            # Overwrite if differs
            edu_org_event = EducationalOrganizationEvent.query.filter_by(event_id=event.id, educational_organization_id=organization.id).first()
            if edu_org_event:
                if edu_org_event.participants != event_data["participants"] or edu_org_event.date_start.strftime("%Y-%m-%d") != event_data["date_start"] or edu_org_event.date_start.strftime("%Y-%m-%d") != event_data["date_end"]:
                    db.session.delete(edu_org_event)
                    db.session.commit()
                    logging.info(f"Overwriting existing relationship between Event({event.id}) and EducationalOrganization({organization.id})")
                    edu_org_event=None

            if not edu_org_event:
                edu_org_event = EducationalOrganizationEvent(
                    educational_organization_id=organization.id,
                    event_id=event.id,
                    participants=event_info["participants"],
                    date_start=event_info["date_start"],
                    date_end=event_info["date_end"],
                )
                db.session.add(edu_org_event)
        db.session.commit()


# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Login page
    """
    if request.method == "POST":
        login = request.form.get("login")

        user = User(login)
        login_user(user)
        session["school_name"] = login

        logging.info(f"User logged in: {login}")

        return redirect(url_for("action"))

    return render_template("sign-in.html")



@app.route("/logout")
@login_required
def logout():
    """
    Logout the user
    """
    logout_user()
    flash("Вы вышли из системы")
    logging.info(f"User logged out.")
    return redirect(url_for("login"))


@app.route("/action", methods=["GET"])
@login_required
def action():
    """
    Action selection page (fill in data/view data)
    """
    return render_template("option.html")


@app.route("/start-survey")
@login_required
def start_survey():
    """
    Processing the "Внести данные" button
    """
    return redirect(url_for("block1"))


@app.route("/block1", methods=["GET", "POST"])
@login_required
def block1():
    """
    Processing the first block of questions
    """
    if request.method == "POST":
        data = {
            "students_number": request.form.get("totalStudents"),
            "class1": request.form.get("class1", type = int, default = 0),
            "class2": request.form.get("class2", type = int, default = 0),
            "class3": request.form.get("class3", type = int, default = 0),
            "class4": request.form.get("class4", type = int, default = 0),
            "class5": request.form.get("class5", type = int, default = 0),
            "class6": request.form.get("class6", type = int, default = 0),
            "class7": request.form.get("class7", type = int, default = 0),
            "class8": request.form.get("class8", type = int, default = 0),
            "class9": request.form.get("class9", type = int, default = 0),
            "class10": request.form.get("class10", type = int, default = 0),
            "class11": request.form.get("class11", type = int, default = 0),
        }
        # Сохраняем выбранные виды спорта и численность
        for sport_name in SPORT_MAPPING.keys():
            checkbox_name = f"{sport_name}Check"
            count_name = f"{sport_name}Count"

            # Проверяем, был ли чекбокс отмечен
            data[checkbox_name] = checkbox_name in request.form
            data[count_name] = request.form.get(count_name, type=int, default=0)
            
        session["block1_data"] = data  # Save data in session
        return redirect(url_for("block2"))

    return render_template("block1.html")


@app.route("/block2", methods=["GET", "POST"])
@login_required
def block2():
    """
    Processing the second block of questions (Events data).
    """
    if request.method == "POST":
        event_data = {}
        index = 0
        MAX_EVENT_IDX = 30

        logging.info("Processing events in block2.")
        while index <= MAX_EVENT_IDX:
            checkbox_value = request.form.get(f"eventCheckbox{index}", "")
            amount_field = request.form.get(f"amountParticipants{index}", "").strip()
            date_start_field = request.form.get(f"eventStart{index}", "").strip()
            date_end_field = request.form.get(f"eventEnd{index}", "").strip()

            logging.info(f"Iteration {index}, checkbox_value: {checkbox_value}, amount_field: {amount_field}, date_start_field: {date_start_field}, date_end_field: {date_end_field}")

            if checkbox_value == "on" and amount_field and date_start_field and date_end_field:
                event_data[index] = {
                    "event_name": base_events[index - 1],
                    "participants": int(amount_field),
                    "date_start": date_start_field,
                    "date_end": date_end_field,
                }
            index += 1

        session["block2_data"] = event_data if event_data else None

        logging.info("Block2 Data:", session.get("block2_data"))

        if request.form.get("action") == "back":
            return redirect(url_for("block1"))
        elif request.form.get("action") == "next":
            return redirect(url_for("block3"))

    return render_template("block2.html")


@app.route("/block3", methods=["GET", "POST"])
@login_required
def block3():
    """
    Processing the third block of questions
    """
    if request.method == "POST":
        event_data = {}
        index = 1
        event_name = request.form.get(f"eventName{index}")
        while event_name:
            amount_field = request.form.get(f"extraAmountParticipants{index}", "").strip()
            date_start_field = request.form.get(f"extraEventStart{index}", "").strip()
            date_end_field = request.form.get(f"extraEventEnd{index}", "").strip()

            event_data[index - 1] = {
                "event_name": event_name,
                "participants": int(amount_field),
                "date_start": date_start_field,
                "date_end": date_end_field,
             }
            index += 1
            event_name = request.form.get(f"eventName{index}")
        session["block3_data"] = event_data if event_data else None

        save_survey_data()

        if request.form.get("action") == "back":
            return redirect(url_for("block2"))
        elif request.form.get("action") == "submit":
            return redirect(url_for("thanks"))

    return render_template("block3.html")


@app.route("/thanks")
@login_required
def thanks():
    """
    "Thank you" page
    """
    return render_template("thanks.html")


@app.route("/view-data", methods=['POST', 'GET'])
@login_required
def view_data():
    """
    View data for the logged-in school.
    """
    # Найти организацию по school_name авторизованного пользователя
    organization = EducationalOrganization.query.filter_by(name=session["school_name"]).first()

    if not organization:
        flash("Данные для вашей школы не найдены.", "error")
        return redirect(url_for("action"))  # Вернуться на стартовую страницу

    # Загрузить данные о мероприятиях для текущей школы
    events = db.session.query(
        Event.name.label("event_name"),
        EducationalOrganizationEvent.participants,
        EducationalOrganizationEvent.date_start,
        EducationalOrganizationEvent.date_end,
    ).join(
        EducationalOrganizationEvent, Event.id == EducationalOrganizationEvent.event_id
    ).filter(
        EducationalOrganizationEvent.educational_organization_id == organization.id
    ).all()

    # Загрузить данные о видах спорта для текущей школы
    sports = db.session.query(
        Sport.name.label("sport_name"),
        EducationalOrganizationSport.members,
    ).join(
        EducationalOrganizationSport, Sport.id == EducationalOrganizationSport.sport_id
    ).filter(
        EducationalOrganizationSport.educational_organization_id == organization.id
    ).all()

    return render_template(
        "school-data.html",
        class1=organization.club_members_grade1,
        class2=organization.club_members_grade2,
        class3=organization.club_members_grade3,
        class4=organization.club_members_grade4,
        class5=organization.club_members_grade5,
        class6=organization.club_members_grade6,
        class7=organization.club_members_grade7,
        class8=organization.club_members_grade8,
        class9=organization.club_members_grade9,
        class10=organization.club_members_grade10,
        class11=organization.club_members_grade11,
        students_number=organization.students_number,
        school_name=organization.name,
        events=events,  # Передаем список мероприятий
        sports=sports,  # Передаем список видов спорта
    )


@app.route("/compare-schools", methods=["GET"])
@login_required
def compare_schools():
    """
    School comparison page
    """
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) != 2:
            exit(1)

        if sys.argv.count("--populate"):
            base_populate_event_table(app, db)
            base_populate_sport_table(app, db)
            logging.info("Populated event and sport tables.")
        else:
            exit(1)

    app.run(debug=True)
