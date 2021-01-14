from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request
)
from pprint import PrettyPrinter


print = PrettyPrinter(indent=4).pprint


app = Flask(__name__)

todos = ['TODO 1', 'TODO 2', 'TODO 3']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))  
    response.set_cookie('user_ip', user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context={
        'user_ip': user_ip,
        'todos': todos
    }
    return render_template('hello.html', **context)

@app.errorhandler(404)
def handle_bad_request(e):
    return render_template('404.html', error=e)

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', error=e)

