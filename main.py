import unittest

from pprint import PrettyPrinter

from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_login import current_user, login_required

from app import create_app
from app.firestore_service import get_users, get_todos
from app.forms import LoginForm


print = PrettyPrinter(indent=4).pprint

app = create_app()

# todos = ['TODO 1', 'TODO 2', 'TODO 3']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))  

    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id

    context={
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    return render_template('hello.html', **context)


# Error handlers
@app.errorhandler(404)
def handle_bad_request(e):
    return render_template('404.html', error=e)

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', error=e)