__author__ = 'Radu'

import os
import sys
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, dirname)

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, session, url_for
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from flask.ext.login import current_user, login_user, LoginManager, UserMixin
from flask.ext.restless import APIManager, ProcessingException

from flask_oauth import OAuth

from models.user import User
app = flask.Flask(__name__, static_folder='webapp', template_folder='webapp', static_url_path='/webapp')
app.db = flask.ext.sqlalchemy.SQLAlchemy(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'asfwe2347^&*%2.e1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password@fbhack.sniffio.com/crosscoapp'

FACEBOOK_APP_ID = '170058559861738'
FACEBOOK_APP_SECRET = 'fbc32b41e6af48cab84a642210be26ed'

db = app.db
api_manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager = LoginManager()
login_manager.setup_app(app)

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)

# Step 4: create the database and add a test user.
db.create_all()
#user1 = User(username=u'test', password=u'test')
#db.session.add(user1)
#db.session.commit()

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

# Step 5: this is required for Flask-Login.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


# Step 7: create endpoints for the application, one for index and one for login
#@app.route('/', methods=['GET'])
#def index():
#    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates a user via an api call
    """
    '''facebook_conn=social.facebook.get_connection()

    username, password = request.args.get('user'), request.args.get('pass')
    matches = User.query.filter_by(username=username,
                                   password=password).all()
    if len(matches) > 0:
        login_user(matches[0])
        return jsonify({"success": True})
        #return redirect(url_for('index'))
    return jsonify({"success": False})'''
    return facebook.authorize(callback='http://hack.sniffio.com:5000'+url_for('appl'))

@app.route('/')
@facebook.authorized_handler
def appl(resp):
    if resp is None:
        return "Not Logged In"
        #return 'Access denied: reason=%s error=%s' % (
        #    request.args['error_reason'],
        #    request.args['error_description']
        #)
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    request.data = {'picture': 'http://graph.facebook.com/%s/picture?type=large' % me.data['username'],
        'first_name': me.data['first_name'], 'last_name': me.data['last_name']}

    session['picture'] = 'http://graph.facebook.com/%s/picture?type=large' % me.data['username']
    session['first_name'] = me.data['first_name']
    session['last_name'] = me.data['last_name']

    return render_template('index.html')

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

def auth_func(**kw):
    if not current_user.is_authenticated():
            raise ProcessingException(message='Not authenticated!')

api_manager.create_api(User, preprocessors=dict(GET_SINGLE=[auth_func],
                                                GET_MANY=[auth_func]),
                            methods=['GET', 'POST', 'DELETE'])

app.run()

