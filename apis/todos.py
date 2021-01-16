from flask_restx import Namespace, fields, Resource

from models.review import TodoDAO

api = Namespace('todos', description='TODO operations')

TodoModel = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
})

DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@api.route('/')
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc('list_todos')
    @api.marshal_list_with(TodoModel)
    def get(self):
        """List all tasks"""
        return DAO.todos

    @api.doc('create_todo')
    @api.expect(TodoModel)
    @api.marshal_with(TodoModel, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @api.doc('get_todo')
    @api.marshal_with(TodoModel)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc('delete_todo')
    @api.response(204, 'Todo deleted')
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return '', 204

    @api.expect(TodoModel)
    @api.marshal_with(TodoModel)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)
