from flask_restx import Namespace, Resource, fields

api = Namespace('tarjetametrobus', description='Tarjeta MetroBus operations')

VerifyModel = api.model('Verify', {
    "number": fields.String(description='Card number'),
    "id": fields.String(description='Identifier'),
    "enabled": fields.Boolean(description="Available"),
    "type": fields.String(description='Contract type'),
})

CardModel = api.model('Card', {
    "ksi": fields.String(description='Key Session Identifier'),
    "number": fields.String(description='Card number'),
    "state": fields.String(description='Contract status'),
    "balance": fields.Fixed(description="Current balance", decimals=2),
    "lastTimeUsed": fields.String(description='Last time used'),
})

UseModel = api.model('Use', {
    "month": fields.String(description='Month name'),
    "uses": fields.Integer(description='Month uses count'),
    "amount": fields.Fixed(description="Month amount", decimals=2),
})

ChargeModel = api.model('Charge', {
    "month": fields.String(description='Month name'),
    "charges": fields.Integer(description='Month charges count'),
    "amount": fields.Fixed(description="Month amount", decimals=2),
})

ResumeModel = api.model('Resume', {
    'uses': fields.List(fields.Nested(UseModel)),
    'charges': fields.List(fields.Nested(ChargeModel)),
})

TrxModel = api.model('Trx', {
    "trxId": fields.Integer(description='Identifier'),
    "action": fields.String(description='# - action'),
    "datetime": fields.String(description="Date and time"),
    "place": fields.String(description="Use place"),
    "amount": fields.Fixed(description="Use amount", decimals=2),
    "balance": fields.Fixed(description="current balance", decimals=2),
})


@api.route('/verify/<int:number>')
@api.response(404, 'Card not found')
@api.param('number', 'card identifier')
class TMInfo(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc('get_verify')
    @api.marshal_with(CardModel)
    def get(self, number):
        """List all tasks"""
        return {
            "card": "0019249279",
            "id": "0",
            "enabled": True,
            "type": 0
        }


@api.route('/info/<int:number>')
@api.response(404, 'Card not found')
@api.param('number', 'card identifier')
class TMInfo(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc('get_balance')
    @api.marshal_with(CardModel)
    def get(self, number):
        """List all tasks"""
        return {
            "ksi": "IDFFBGAD19670184657939712547",
            "number": "0019449278",
            "status": "Contrato Activo",
            "balance": "2.05",
            "lastTimeUsed": "30/06/2020 12:39"
        }


@api.route('/resume/<int:number>')
@api.response(404, 'Card not found')
@api.param('number', 'card identifier')
class TMResume(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc('get_resume')
    @api.marshal_with(ResumeModel)
    def get(self, number):
        """List all tasks"""
        return {
            "uses": [
                {"month": "Julio", "amount": "0.00", "uses": "0"},
                {"month": "Junio", "amount": "5.20", "uses": "12"},
                {"month": "Mayo", "amount": "3.00", "uses": "7"}
            ],
            "charges": [
                {"month": "Julio", "amount": "0.00", "charges": "0"},
                {"month": "Junio", "amount": "0.00", "charges": "0"},
                {"month": "Mayo", "amount": "0.00", "charges": "0"}
            ]
        }


@api.route('/trx/<int:number>')
@api.response(404, 'Card not found')
@api.param('number', 'card identifier')
class TMTrx(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc('get_trx')
    @api.marshal_with(ResumeModel)
    def get(self, number):
        """List all tasks"""
        return {
            "uses": [
                {"month": "Julio", "amount": "0.00", "uses": "0"},
                {"month": "Junio", "amount": "5.20", "uses": "12"},
                {"month": "Mayo", "amount": "3.00", "uses": "7"}
            ],
            "charges": [
                {"month": "Julio", "amount": "0.00", "charges": "0"},
                {"month": "Junio", "amount": "0.00", "charges": "0"},
                {"month": "Mayo", "amount": "0.00", "charges": "0"}
            ]
        }
