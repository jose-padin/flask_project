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


from app.firestore_service import get_user
from app.forms import LoginForm
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

            if password_from_db == password:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)

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