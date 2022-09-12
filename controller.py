from flask import Flask, render_template
from flask_graphql import GraphQLView

app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def index():
    return render_template('index.html')





if __name__ == "__main__":
    app.run(port=5002, debug=True)

