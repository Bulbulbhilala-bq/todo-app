# Doist — Flask Todo App

A clean, full-stack todo app with a login page and full task management.

## Quick Start

```bash
# 1. Install Flask
pip install flask

# 2. Run the app
python app.py

# 3. Open in browser
# http://localhost:5000
```

## Login Credentials (Demo)
- **Username:** `demo`
- **Password:** `demo123`

## Features
- Demo login / logout
- Add tasks with priority (High / Medium / Low)
- Toggle tasks complete / incomplete
- Edit task text and priority via modal
- Delete tasks
- Filter by All / Pending / Done / High Priority
- Live stats (total, done, pending counts)
- Keyboard shortcuts: Enter to add, Escape to close modal

## Project Structure
```
todo_app/
├── app.py               # Flask backend + REST API
├── requirements.txt
└── templates/
    ├── login.html       # Login page
    └── todos.html       # Main todo dashboard
```

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/todos` | List all todos |
| POST | `/api/todos` | Create a todo |
| PUT | `/api/todos/<id>` | Update a todo |
| DELETE | `/api/todos/<id>` | Delete a todo |

> Note: Todos are stored in-memory and reset when the server restarts.
> For persistence, swap `todos_store` with a SQLite database using Flask-SQLAlchemy.
