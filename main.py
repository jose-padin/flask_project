import unittest

from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from pprint import PrettyPrinter

from app import create_app
from app.forms import LoginForm


print = PrettyPrinter(indent=4).pprint

app = create_app()

todos = ['TODO 1', 'TODO 2', 'TODO 3']


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
def hello():
    user_ip = session.get('user_ip', None)
    username = session.get('username', None)

    context={
        'user_ip': user_ip,
        'todos': todos,
        'username': username
    }

    return render_template('hello.html', **context)

@app.errorhandler(404)
def handle_bad_request(e):
    return render_template('404.html', error=e)

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', error=e)

