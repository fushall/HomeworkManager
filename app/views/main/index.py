# coding: utf8


from . import main

from ...models.task import TaskModel

@main.route('/')
def index_view():
    tasks = TaskModel.query.order_by(TaskModel.id.desc())
    return main.render_template('index.html', tasks=tasks)
