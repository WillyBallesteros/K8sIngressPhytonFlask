import logging
from dotenv import load_dotenv

from src.models.model import initdb
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
import os

app = Flask(__name__)
app.register_blueprint(operations_blueprint)
if os.getenv('ENV') != 'test':
  logging.warning(f'initdb[antes]')
  initdb()
  logging.warning(f'initdb[despues]')

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
