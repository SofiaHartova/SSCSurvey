from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from db.db import db
from db.models import EducationalOrganization, Event


app = Flask(__name__)
login = LoginManager(app)
app.secret_key = "your_secret_key"  # Key for sessions to store user data
login.login_view = "login"

# Temporary user store for demo purposes
users = {"admin": {"password": "password"}}


# User class implementing UserMixin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id


@login.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None


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

    if block1_data:
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
        db.session.add(organization)
        db.session.commit()

    if block2_data:
        for event_data in block2_data.values():
            event = Event(
                name=event_data["event_name"],
                participants=event_data["participants"],
                date_start=event_data["date_start"],
                date_end=event_data["date_end"],
            )
            db.session.add(event)
        db.session.commit()

    if block3_data:
        for event_name, event_info in block3_data.items():
            event = Event(
                name=event_name,
                participants=event_info["participants"],
                date_start=event_info["event_date_start"],
                date_end=event_info["event_date_end"],
            )
            db.session.add(event)
        db.session.commit()


# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Login page
    """
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login in users and users[login]["password"] == password:
            user = User(login)
            login_user(user)
            session["school_name"] = login
            return redirect(url_for("action"))
        else:
            flash("Неверный логин или пароль!")

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
            "class1": request.form.get("class1"),
            "class2": request.form.get("class2"),
            "class3": request.form.get("class3"),
            "class4": request.form.get("class4"),
            "class5": request.form.get("class5"),
            "class6": request.form.get("class6"),
            "class7": request.form.get("class7"),
            "class8": request.form.get("class8"),
            "class9": request.form.get("class9"),
            "class10": request.form.get("class10"),
            "class11": request.form.get("class11"),
        }
        session["block1_data"] = data  # Save data in session
        return redirect(url_for("block2"))

    return render_template("block1.html")


@app.route("/block2", methods=["GET", "POST"])
@login_required
def block2():
    """
    Processing the second block of questions
    """
    if request.method == "POST":
        event_data = {
            "event1": {
                "event_name": request.form.get("event1"),
                "participants": request.form.get("participants1"),
                "date_start": request.form.get("date_start1"),
                "date_end": request.form.get("date_end1"),
            },
            # Todo: add other events
        }
        session["block2_data"] = event_data  # Save data in session
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
            "eventName1": {
                "name": request.form.get("eventName1"),
                "participants": request.form.get("participants1"),
                "event_date_start": request.form.get("event_date_start1"),
                "event_date_end": request.form.get("event_date_end1"),
            }
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
            students_number=session.get("students_number", 0),
        )


@app.route("/compare-schools", methods=["GET"])
@login_required
def compare_schools():
    """
    School comparison page
    """
    pass


if __name__ == "__main__":
    app.run(debug=True)
