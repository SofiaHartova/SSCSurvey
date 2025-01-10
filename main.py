from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from db.db import db
from db.models import EducationalOrganization, Event, EducationalOrganizationEvent
from db.events import base_populate_event_table
from db.sports import base_populate_sport_table


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
        return

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
        name = school_name,
    )

    # If such educational organization already submited data then ignore this try
    exists = EducationalOrganization.query.filter_by(name=school_name).first()
    if exists:
        # TODO: Inform user that's ignored
        return

    db.session.add(organization)
    db.session.commit()

    if block2_data:
        for event_data in block2_data.values():
            event = Event(
                name=event_data["event_name"],
            )
            print(event_data)

            # Insert event uniquely
            exists = Event.query.filter_by(name=event.name).first()
            if not exists:
                db.session.add(event)
                db.session.commit()

            edu_org_event = EducationalOrganizationEvent(
                educational_organization_id=organization.id,
                event_id=event.id,
                participants=event_data["participants"],
                date_start=event_data["date_start"],
                date_end=event_data["date_end"],
            )
            db.session.add(edu_org_event)
        db.session.commit()

    if block3_data:
        for event_name, event_info in block3_data.items():
            event = Event(
                name=event_data["event_name"],
            )
            edu_org_event = EducationalOrganizationEvent(
                educational_organization_id=organization.id,
                event_id=event.id,
                participants=event_data["participants"],
                date_start=event_data["date_start"],
                date_end=event_data["date_end"],
            )

            # Insert event uniquely
            exists = Event.query.filter_by(name=event.name).first()
            if not exists:
                db.session.add(event)
                db.session.commit()

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

        return redirect(url_for("action"))
        # password = request.form.get("password")

        # if login in users and users[login]["password"] == password:
        #     user = User(login)
        #     login_user(user)
        #     session["school_name"] = login
        #     return redirect(url_for("action"))
        # else:
        #     flash("Неверный логин или пароль!")

    return render_template("sign-in.html")



@app.route("/logout")
@login_required
def logout():
    """
    Logout the user
    """
    logout_user()
    flash("Вы вышли из системы")
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
        session["block1_data"] = data  # Save data in session
        return redirect(url_for("block2"))

    return render_template("block1.html")


@app.route("/block2", methods=["GET", "POST"])
@login_required
def block2():
    if request.method == "POST":
        event_data = {}
        index = 1
        MAX_EVENTS = 31

        print("Начинаем обработку событий")

        while index <= MAX_EVENTS:
            checkbox_value = request.form.get(f"eventCheckbox{index}")
            amount_field = request.form.get(f"amountParticipants{index}", "").strip()
            date_start_field = request.form.get(f"eventStart{index}", "").strip()
            date_end_field = request.form.get(f"eventEnd{index}", "").strip()

            print(f"Итерация {index}, checkbox_value: {checkbox_value}, amount_field: {amount_field}, date_start_field: {date_start_field}, date_end_field: {date_end_field}")

            if checkbox_value == "on" and (amount_field or date_start_field or date_end_field):
                event_data[index] = {
                    "event_name": f"Мероприятие {index}",
                    "participants": amount_field,
                    "date_start": date_start_field,
                    "date_end": date_end_field,
                }
            index += 1

        print(f"Обработанные данные мероприятий: {event_data}")

        session["block2_data"] = event_data if event_data else None

        print("Block2 Data:", session.get("block2_data"))

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
        event_details = {
            # "eventName1": {
            #     "name": request.form.get("eventName1"),
            #     "participants": request.form.get("extraAmountParticipants1"),
            #     "event_date_start": request.form.get("extraEventStart1"),
            #     "event_date_end": request.form.get("extraEventEnd1"),
            # }
            # Todo: add other events
        }
        session["block3_data"] = event_details

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


@app.route("/view-data")
@login_required
def view_data():
    """
    View data for the logged-in school.
    """
    # Найти организацию по school_name авторизованного пользователя
    organization = EducationalOrganization.query.filter_by(school_name=session["school_name"]).first()

    if not organization:
        flash("Данные для вашей школы не найдены.", "error")
        return redirect(url_for("action"))  # Вернуться на стартовую страницу
    
    # Передаем данные в шаблон
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
    )


@app.route("/school-data", methods=["GET", "POST"])
@login_required
def school_data():
    """
    School data page
    """
    if request.method == "POST":
        return render_template(
            "school-data.html",
            class1=session["block1_data"]["class1"],
            class2=session["block1_data"]["class2"],
            class3=session["block1_data"]["class3"],
            class4=session["block1_data"]["class4"],
            class5=session["block1_data"]["class5"],
            class6=session["block1_data"]["class6"],
            class7=session["block1_data"]["class7"],
            class8=session["block1_data"]["class8"],
            class9=session["block1_data"]["class9"],
            class10=session["block1_data"]["class10"],
            class11=session["block1_data"]["class11"],
            students_number=session["block1_data"]["students_number"],
        )


@app.route("/compare-schools", methods=["GET"])
@login_required
def compare_schools():
    """
    School comparison page
    """
    pass


if __name__ == "__main__":
    base_populate_event_table(app, db)
    base_populate_sport_table(app, db)
    app.run(debug=True)
