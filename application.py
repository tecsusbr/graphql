# -*- encoding: utf-8 -*-

import flask
import schema
import flask_cors

from flask_graphql import GraphQLView
from flask import render_template
from models import db_session

app = flask.Flask(__name__,
                  static_folder='static',
                  template_folder='templates')

app.debug = True
flask_cors.CORS(app, automatic_options=True)



app.add_url_rule('/graphql',
       view_func=GraphQLView.as_view('graphql',
       schema=schema.schema,
       graphiql=True))

app.add_url_rule('/graphqljs',
       view_func=GraphQLView.as_view('graphqljs',
       schema=schema.schema,
       graphiql=False))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db')
def db():
    """Testing database connections"""
    result = db_session.execute("SELECT * FROM departments")
    names = [row[0] for row in result]
    return "<HTML><body><div>{}</div></body></HTML>".format("<br>".join(names))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()