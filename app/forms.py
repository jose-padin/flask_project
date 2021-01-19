from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Send')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password confirm', validators=[DataRequired()])
    submit = SubmitField('Send')
 
    def check_password(self, password, password2):
        if password == password2:
            return True
        return False


class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create to-do')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Delete')


class EditTodoForm(FlaskForm):
    submit = SubmitField('Done')
