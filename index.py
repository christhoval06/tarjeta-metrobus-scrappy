import random

from crochet import setup
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix
from apis import api

setup()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

api.init_app(app)


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def _handle_api_error(ex):
    return jsonify(ex.to_dict()) if request.path.startswith('/api/') else ex


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=random.randint(2000, 9000)
    )
