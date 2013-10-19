__author__ = 'Radu'

from flask import render_template, request, session, url_for
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from flask.ext.login import current_user, login_user, LoginManager, UserMixin
from flask.ext.restless import ProcessingException

from crossco import app
from crossco.models.models import User

@app.login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

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
    return app.fb.authorize(callback='http://hack.sniffio.com:5000'+url_for('appl'))

@app.route('/')
@app.fb.authorized_handler
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

@app.fb.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

def auth_func(**kw):
    if not current_user.is_authenticated():
            raise ProcessingException(message='Not authenticated!')

app.api_manager.create_api(User, preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]),
                           methods=['GET', 'POST'])
