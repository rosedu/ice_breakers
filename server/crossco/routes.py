__author__ = 'Radu'

import json
from flask import render_template, request, session, url_for, redirect, make_response, jsonify
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from flask.ext.login import current_user, login_user, logout_user, LoginManager, UserMixin
from flask.ext.restless import ProcessingException


from crossco import app
from crossco.models.models import *
from crossco.handlers.handler import handler

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
    return app.fb.authorize(callback='http://'+request.host+url_for('fbcheck'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return redirect("/")

@app.route('/fbcheck')
@app.fb.authorized_handler
def fbcheck(resp):
    if resp is None:
        return  render_template('index.html')
        #return 'Access denied: reason=%s error=%s' % (
        #    request.args['error_reason'],
        #    request.args['error_description']
        #)
    session['oauth_token'] = (resp['access_token'], '')
    me = app.fb.get('/me')

    '''request.data = {'picture': 'http://graph.facebook.com/%s/picture?type=large' % me.data['username'],
        'first_name': me.data['first_name'], 'last_name': me.data['last_name']}
    session['picture'] = 'http://graph.facebook.com/%s/picture?type=large' % me.data['username']
    session['first_name'] = me.data['first_name']
    session['last_name'] = me.data['last_name']'''

    matches = User.query.filter_by(fb_id=me.data['id']).all()
    if not matches:
        #Add new user
        user = User(fb_id=me.data['id'], fb_data=json.dumps(me.data))
        app.db.session.add(user)
    else:
        user = matches[0]
        user.fb_data=json.dumps(me.data)
    app.db.session.commit()
    login_user(user)
    return redirect("/")

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    #if current_user.is_authenticated():
    #    resp.set_cookie('uid', str(current_user.id), httponly=False)
    return resp

@app.fb.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

app.api_manager.create_api(User,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(User, **kw)],
                                              GET_MANY=[lambda **kw: handler(User, **kw)]),
                           methods=['GET', 'POST'])
app.api_manager.create_api(Action,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Action, **kw)],
                                              GET_MANY=[lambda **kw: handler(Action, **kw)]),
                           methods=['GET', 'POST'])
app.api_manager.create_api(Service,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Service, **kw)],
                                              GET_MANY=[lambda **kw: handler(Service, **kw)]),
                           methods=['GET', 'POST'])

app.api_manager.create_api(Category,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Category, **kw)],
                                              GET_MANY=[lambda **kw: handler(Category, **kw)]),
                           methods=['GET', 'POST'])
#app.api_manager.create_api(Action, preprocessors=dict(GET_SINGLE=[get_actions], GET_MANY=[get_actions]),
#                           methods=['GET', 'POST'])