"""
unit test for controller.py

uses pytest
"""

from urllib import response
import pytest
import sys
sys.path.append('..')
from controller import app
from flask import Flask, render_template

print("import successful")

flask_app = Flask(__name__)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestController:
    """
    GIVEN the controller Flask application
    WHEN the '/hello' page is requested (GET)
    THEN check that the response is valid
    """
    def test_hello(self, client):
        app.testing = True
        response = client.get('/hello')

        assert response.status_code == 200
        assert response.data == b'Hello World!'
        

    """
    GIVEN the controller Flask application
    WHEN the '/' page is requested (GET)
    THEN render the index.html template
    """
    def test_index(self, client):
        app.testing = True
        response = client.get('/')

        assert response.status_code == 200
        assert response.data.decode('utf-8') == render_template('index.html')
        