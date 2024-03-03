import os
from dotenv import load_dotenv
import logging
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .errors.errors import ApiError
from .blueprints.operations import operations_blueprint
from .models.model import initdb

app = Flask(__name__)
app.register_blueprint(operations_blueprint)

if os.getenv('ENV') != 'test':
  initdb()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
