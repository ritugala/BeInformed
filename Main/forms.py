from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,TextAreaField
from wtforms.validators import DataRequired,  ValidationError
from Main.models import Student
from flask_login import current_user




class LoginForm(FlaskForm):

    #email = StringField('Email', validators = [DataRequired(),Email()])
    id = IntegerField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AddUser(FlaskForm):

    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField("Submit")
    def validate_id(self, id):
        student = Student.query.filter_by(id = id.data).first()
        if student:
            raise ValidationError("This ID is taken choose another one")


class UpdateAccountForm(FlaskForm):

    name = StringField('Name', validators=[])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Update")

class PostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    #time_posted = StringField('Time')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
