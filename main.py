from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

app = Flask(__name__)
login = LoginManager(app)
app.secret_key = 'your_secret_key' # Key for sessions to store user data
login.login_view = 'login'

# Temporary user store for demo purposes
users = {'admin': {'password': 'password'}}

#User class implementing UserMixin
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


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Login page
    """
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if login in users and users[login]['password'] == password:
            user = User(login) 
            login_user(user)
            session['user'] = login
            return redirect(url_for('action'))
        else:
            flash("Неверный логин или пароль!")

    return render_template('sign-in.html')


@app.route('/logout')
@login_required
def logout():
    """
    Logout the user
    """
    logout_user()
    flash("Вы вышли из системы")
    return redirect(url_for('login'))


@app.route('/action', methods=['GET'])
@login_required
def action():
    """
    Action selection page (fill in data/view data)
    """
    return render_template('option.html')


@app.route('/start-survey')
@login_required
def start_survey():
    """
    Processing the "Внести данные" button
    """
    return redirect(url_for('block1'))


@app.route('/block1', methods=['GET', 'POST'])
@login_required
def block1():
    """
    Processing the first block of questions
    """
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


@app.route('/block2', methods=['GET', 'POST'])
@login_required
def block2():
    """
    Processing the second block of questions
    """
    if request.method == 'POST':
        event_data = {
            'event1': request.form.get('event1'),
            'participants1': request.form.get('participants1'),
            'date1': request.form.get('date1'),
            # Todo: add other events
        }
        session['block2_data'] = event_data  # Save data in session
        if request.form.get('action') == 'back':
            return redirect(url_for('block1'))
        elif request.form.get('action') == 'next':
            return redirect(url_for('block3'))

    return render_template('block2.html')


@app.route('/block3', methods=['GET', 'POST'])
@login_required
def block3():
    """
    Processing the third block of questions
    """
    if request.method == 'POST':
        event_details = {
            'eventName1': request.form.get('eventName1'),
            'participants1': request.form.get('participants1'),
            'eventDate1': request.form.get('eventDate1'),
            # Todo: add other events
        }
        session['block3_data'] = event_details
        if request.form.get('action') == 'back':
            return redirect(url_for('block2'))
        elif request.form.get('action') == 'submit':
            return redirect(url_for('thanks'))

    return render_template('block3.html')


@app.route('/thanks')
@login_required
def thanks():
    """
    "Thank you" page
    """
    return render_template("thanks.html")


@app.route('/view-data')
@login_required
def view_data():
    """
    Processing the "Посмотреть данные" button
    """
    pass


@app.route('/school-data', methods=['GET'])
@login_required
def school_data():
    """
    School data page
    """
    pass


@app.route('/compare-schools', methods=['GET'])
@login_required
def compare_schools():
    """
    School comparison page
    """
    pass

if __name__ == '__main__':
    app.run(debug=True)
