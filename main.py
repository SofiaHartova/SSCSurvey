from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from db.db import db
from db.models import EducationalOrganization, Event


app = Flask(__name__)
app.secret_key = 'your_secret_key' # Key for sessions to store user data

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:sscsserverpostgres@sscsurvey.ru:5432/sscs_db?connect_timeout=10&sslmode=prefer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def save_survey_data():
    block1_data = session.get('block1_data')
    block2_data = session.get('block2_data')
    block3_data = session.get('block3_data')
    if block1_data:
        organization = EducationalOrganization(
            students_number=block1_data['totalStudents'],
            club_members_grade1=block1_data['class1'],
            club_members_grade2=block1_data['class2'],
            club_members_grade3=block1_data['class3'],
            club_members_grade4=block1_data['class4'],
            club_members_grade5=block1_data['class5'],
            club_members_grade6=block1_data['class6'],
            club_members_grade7=block1_data['class7'],
            club_members_grade8=block1_data['class8'],
            club_members_grade9=block1_data['class9'],
            club_members_grade10=block1_data['class10'],
            club_members_grade11=block1_data['class11']
        )
        db.session.add(organization)
        db.session.commit()
    if block2_data:
        for event_data in block2_data.values():
            event = Event(
                name=event_data['event_name'],
                participants=event_data['participants'],
                date=event_data['date']
            )
            db.session.add(event)
        db.session.commit()
    if block3_data:
        for event_name, event_info in block3_data.items():
            event = Event(
                name=event_name,
                participants=event_info['participants'],
                date=event_info['eventDate']
            )
            db.session.add(event)
        db.session.commit()

# Login page
@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if login == 'admin' and password == 'password':
            session['user'] = login
            return redirect(url_for('action'))
        else:
            return "Неверный логин или пароль!"

    return render_template('sign-in.html')

# Action selection page (fill in data/view data)
@app.route('/action', methods=['GET'])
def action():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('option.html')

# Processing the "Внести данные" button
@app.route('/start-survey')
def start_survey():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('block1'))

# First block of questions
@app.route('/block1', methods=['GET', 'POST'])
def block1():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = {
            'totalStudents': request.form.get('totalStudents'),
            'class1': request.form.get('class1'),
            'class2': request.form.get('class2'),
            'class3': request.form.get('class3'),
            'class4': request.form.get('class4'),
            'class5': request.form.get('class5'),
            'class6': request.form.get('class6'),
            'class7': request.form.get('class7'),
            'class8': request.form.get('class8'),
            'class9': request.form.get('class9'),
            'class10': request.form.get('class10'),
            'class11': request.form.get('class11'),
        }
        session['block1_data'] = data  # Save data in session
        return redirect(url_for('block2'))

    return render_template('block1.html')

# Second block of questions
@app.route('/block2', methods=['GET', 'POST'])
def block2():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        event_data = {
            'event1': {
                'event_name': request.form.get('event1'),
                'participants': request.form.get('participants1'),
                'date': request.form.get('date1')
            },
            # Todo: add other events
        }
        session['block2_data'] = event_data  # Save data in session
        if request.form.get('action') == 'back':
            return redirect(url_for('block1'))
        elif request.form.get('action') == 'next':
            return redirect(url_for('block3'))

    return render_template('block2.html')

# Third block of questions
@app.route('/block3', methods=['GET', 'POST'])
def block3():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        event_details = {
            'eventName1': {
                'name': request.form.get('eventName1'),
                'participants': request.form.get('participants1'),
                'eventDate': request.form.get('eventDate1')
            }
            # Todo: add other events
        }
        session['block3_data'] = event_details

        save_survey_data()

        if request.form.get('action') == 'back':
            return redirect(url_for('block2'))
        elif request.form.get('action') == 'submit':
            return redirect(url_for('thanks'))

    return render_template('block3.html')

# Thank you page
@app.route('/thanks')
def thanks():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("thanks.html")

# Processing the "Посмотреть данные" button
@app.route('/view-data')
def view_data():
    pass

# School data page
@app.route('/school-data', methods=['GET'])
def school_data():
    pass

# School comparison page
@app.route('/compare-schools', methods=['GET'])
def compare_schools():
    pass

if __name__ == '__main__':
    app.run(debug=True)
