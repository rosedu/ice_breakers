__author__ = 'Radu'
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth
from flask.ext.restless import APIManager
from flask.ext.login import current_user, login_user, LoginManager, UserMixin

from crossco.util.singleton import Singleton
from crossco.config import config

class CApp(flask.Flask):
    """
    Main Crossco app. Made singleton to force one instance per server.
    """
    __metaclass__ = Singleton
    def __init__(self, import_name='', static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        flask.Flask.__init__(self, import_name,
                                     template_folder=template_folder)
        self.config.update(config)
        self.db = flask.ext.sqlalchemy.SQLAlchemy(self)
        self.fb = OAuth().remote_app('facebook',
                base_url='https://graph.facebook.com/',
                request_token_url=None,
                access_token_url='/oauth/access_token',
                authorize_url='https://www.facebook.com/dialog/oauth',
                consumer_key=self.config['FACEBOOK_APP_ID'],
                consumer_secret=self.config['FACEBOOK_APP_SECRET'],
                request_token_params={'scope': 'email'})
        self.api_manager = APIManager(self, flask_sqlalchemy_db=self.db)
        self.login_manager = LoginManager()
        self.login_manager.setup_app(self)

    def run(self, host=None, port=None, debug=None, **options):
        self.db.create_all()
        flask.Flask.run(self, host, port, debug, **options)


app = CApp(__name__, static_folder='webapp', template_folder='webapp', static_url_path='/webapp')