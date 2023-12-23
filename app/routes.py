# app/routes.py

from flask import render_template, request, redirect, url_for
from app import app, db

# # Example route for the home page
# @app.route('/')
# def home():
#     return 'Hello, World!'

# # Example route for displaying a list of tasks
# @app.route('/tasks')
# def task_list():
#     tasks = Task.query.all()
#     return render_template('tasks/list.html', tasks=tasks)

# # Example route for adding a new task
# @app.route('/tasks/add', methods=['POST'])
# def add_task():
#     title = request.form.get('title')
#     new_task = Task(title=title)
#     db.session.add(new_task)
#     db.session.commit()
#     return redirect(url_for('task_list'))
