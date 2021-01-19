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
from app.firestore_service import (
    create_todo,
    delete_todo,
    edit_todo,
    get_todos,
    get_users
)
from app.forms import (
    DeleteTodoForm,
    EditTodoForm,
    LoginForm,
    TodoForm
)


print = PrettyPrinter(indent=4).pprint

app = create_app()


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

    context={
        'delete_form': DeleteTodoForm(),
        'edit_form': EditTodoForm(),
        'todos': get_todos(user_id=current_user.id),
        'username': current_user.id,
        'user_ip': session.get('user_ip')
    }

    return render_template('hello.html', **context)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TodoForm()

    context = {
        'form': form
    }
    
    username = session.get('username')

    if request.method == 'POST':
        create_todo(user_id=username, description=form.description.data)
        return redirect(url_for('hello'))

    return render_template('add_todo.html', **context)


@app.route('/todos/edit/<todo_id>/<done>', methods=['GET', 'POST'])
def edit(todo_id, done):
    done = True if done == 'True' else False
    done = bool(done)
    user_id = current_user.id
    edit_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))
        

@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    return redirect(url_for('hello'))


# Error handlers
@app.errorhandler(404)
def handle_bad_request(e):
    return render_template('404.html', error=e)

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', error=e)