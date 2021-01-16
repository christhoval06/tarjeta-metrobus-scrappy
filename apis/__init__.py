from flask_restx import Api

from .tarjetametrobus import api as tarjetametrobus
from .todos import api as todos
from .amazon import api as amazon

api = Api(
    title="Christhoval's Services",
    version='0.0.1',
    description='This is our sample API'
)

api.add_namespace(todos)
api.add_namespace(tarjetametrobus)
api.add_namespace(amazon)
