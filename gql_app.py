from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from model import db_session, Base, engine
from seed_db import *
from flask_cors import CORS

app = Flask(__name__) 
app.debug = True 
CORS(app)

Base.metadata.create_all(bind=engine) # create tables in database if they don't exist, starts database session


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    os.system('python seed_db.py')
    app.run(port=5001, debug=True, host='0.0.0.0')
