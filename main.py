from flask import Flask, render_template

app = Flask(__name__)

# Login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template("sign-in.html")

# Processing login and password
@app.route('/login', methods=['POST'])
def login():
    pass

# Action selection page (fill in data/view data)
@app.route('/action', methods=['GET'])
def action_page():
    return render_template("option.html")

# First block of questions
@app.route('/questions1', methods=['POST'])
def questions1():
    pass

# Second block of questions
@app.route('/questions2', methods=['POST'])
def questions2():
    pass

# Third block of questions
@app.route('/questions3', methods=['POST'])
def questions3():
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
