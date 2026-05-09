
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from datetime import datetime
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = 'demo_secret_key_change_this'

# =====================
# Google OAuth Setup
# =====================
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=('GOOGLE_CLIENT_ID'),
     client_secret=('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# In-memory todo store per user (email se identify)
todos_store = {}

def get_todos():
    user = session.get('email')
    if user not in todos_store:
        todos_store[user] = []
    return todos_store[user]

def save_todos(todos):
    todos_store[session['email']] = todos

# =====================
# Auth Routes
# =====================

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('todos'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('todos'))
    return render_template('login.html')

@app.route('/google-login')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/google/callback')
def google_callback():
    token = google.authorize_access_token()
    userinfo = token.get('userinfo')
    if userinfo:
        session['email'] = userinfo['email']
        session['name'] = userinfo.get('name', userinfo['email'])
        session['picture'] = userinfo.get('picture', '')
    return redirect(url_for('todos'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =====================
# Todo Routes
# =====================

@app.route('/todos')
def todos():
    if 'email' not in session:
        return redirect(url_for('login'))
    todo_list = get_todos()
    return render_template('todos.html',
                           todos=todo_list,
                           username=session.get('name'),
                           picture=session.get('picture'))

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(get_todos())

@app.route('/api/todos', methods=['POST'])
def api_add_todo():
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    todos = get_todos()
    new_todo = {
        'id': len(todos) + 1,
        'text': data.get('text', ''),
        'done': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    todos.append(new_todo)
    save_todos(todos)
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    todos = get_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            save_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    todos = get_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)