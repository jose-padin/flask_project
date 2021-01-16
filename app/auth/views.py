from flask import (
    request,
    session,
    flash,
    render_template,
    redirect,
    url_for
)


from app.forms import LoginForm

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    context = {
        'login_form': LoginForm()
    }

    if request.method == 'POST':
        session['username'] = login_form.username.data
        flash('Username registered!')
        return redirect(url_for('index'))

    return render_template('login.html', **context)