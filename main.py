from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c99d2943ab28da8b956686f2dfc53531'
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(35), nullable =False)
    username = db.Column(db.String(20), unique = True, nullable =False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), default = 'photo.jpeg')
    password = db.Column(db.String(60), nullable = False)
    year = db.Column(db.String(20), nullable=False)
    #dob = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable =False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), default = 'photo.jpeg')
    password = db.Column(db.String(60), nullable = False)
    course = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.course}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('studenthome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('studentlogin.html', title='Login', form=form)

@app.route('/facultylogin')
def facultylogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('facultyhome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('facultylogin.html', title='Login', form=form)

@app.route('/studenthome')
def studenthome():
    return render_template(studenthome.html)

@app.route('/facultyhome')
def facultyhome():
    return render_template(facultyhome.html)

if __name__ == '__main__':
    app.run(debug=True)
