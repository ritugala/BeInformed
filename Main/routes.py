from flask import render_template, url_for, flash, redirect, request
from Main.models import Student, Faculty
from Main.forms import LoginForm, AddUser, UpdateAccountForm, PostForm
from Main import app, db, bcrypt
from Main.models import Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    # if current_user.is_authenticated:
    #     return redirect(url_for('facultylogin'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id = form.id.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('studenthome'))
        else:
            flash('Login Unsuccessful. Please check id and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/facultylogin', methods = ['GET', 'POST'])
def facultylogin():
    form = LoginForm()
    if form.validate_on_submit():

        flash('Login Unsuccessful. Please check id and password', 'danger')
    return render_template('facultylogin.html', title='Login', form=form)

@app.route('/studenthome')
def studenthome():
    posts = Post.query.all()
    return render_template('studenthome.html',posts = posts)

@app.route('/facultyhome')
def facultyhome():
    return render_template('facultyhome.html')


@app.route('/adduser', methods = ['GET', 'POST'])
def AddMember():
    form = AddUser()
    if form.validate_on_submit():
        student = Student(name = form.name.data, id = form.id.data, password = bcrypt.generate_password_hash(form.name.data + str(form.id.data % 100)).decode('utf-8'))
        db.session.add(student)
        db.session.commit()

    return render_template('adduser.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
    image_file = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)



@app.route('/facultypost/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been updated successfully', 'success')
        return redirect(url_for('studenthome'))
    return render_template('create_post.html', title = 'New Post', form = form)
