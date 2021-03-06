import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluations.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)


class evaluations(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Text())

    def __init__(self, name, value):
        self.name = name
        self.value = value


def database_initialization_sequence():
    db.create_all()
    test_rec = evaluations(
            'Initial test of json',
            '{}')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['value']:
            flash('Please enter all the fields', 'error')
        else:
            evaluation = evaluations(
                    request.form['name'],
                    request.form['value'])

            db.session.add(evaluation)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('index.html', evaluations=evaluations.query.all())

@app.route('/new', methods=['POST'])
def new():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            evaluation = evaluations(
                    request.form['name'],
                    '[]') # Need this to be valid json so it doesn't break the javascript

            db.session.add(evaluation)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('index.html', evaluations=evaluations.query.all())

@app.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['value'] or not request.form['id']:
            flash('Please enter all the fields', 'error')
        else:
            evaluation_id = request.form['id']
            evaluation = evaluations.query.filter_by(id=evaluation_id).first()
            evaluation.name = request.form['name']
            evaluation.value = request.form['value']
            db.session.commit()
            flash('Record was succesfully updated')
            return redirect(url_for('view',id=evaluation_id))
    if request.method == 'GET':
        evaluation_id = request.args['id']
    return render_template('view.html', evaluation=evaluations.query.filter_by(id=evaluation_id).first())



if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0',threaded=True) 
