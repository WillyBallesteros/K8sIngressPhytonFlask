import os
from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .errors.errors import ApiError
from .blueprints.operations import operations_blueprint

app = Flask(__name__)
app.register_blueprint(operations_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
