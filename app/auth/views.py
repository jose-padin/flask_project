from flask import (
    request,
    session,
    flash,
    render_template,
    redirect,
    url_for
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from werkzeug.security import check_password_hash, generate_password_hash


from app.firestore_service import get_user, user_put
from app.forms import LoginForm, SignupForm
from app.models import UserData, UserModel

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    login_form = LoginForm()

    context = {
        'login_form': LoginForm()
    }

    if request.method == 'POST':
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(user_id=username)

        if user_doc.to_dict():
            password_from_db = user_doc.to_dict()['password']

            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)

                session['username'] = login_form.username.data
                
                redirect(url_for('hello'))
                flash('Welcome back!')
            else:
                flash('Info do not match')
        else:
            flash('Username does not exist')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('login')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    context = {
        'form': form
    }

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data

        if form.check_password(password, password2):
            user_doc = get_user(username)
            
            if user_doc.to_dict() is None:
                user_data = UserData(
                    username=username,
                    password=generate_password_hash(password)
                )

                user_put(user_data)

                user = UserModel(user_data)
                return redirect(url_for('auth.login'))
            else:
                flash('User already exists.')
        else:
            flash('Passwords didn\' match.')

    return render_template('signup.html', **context)