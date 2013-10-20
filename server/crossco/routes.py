__author__ = 'Radu'

import json
from flask import render_template, request, session, url_for, redirect, make_response, jsonify
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from flask.ext.login import current_user, login_user, logout_user, LoginManager, UserMixin
from flask.ext.restless import ProcessingException

from crossco import app
from crossco.models.models import *
from crossco.handlers.handler import handler, post_handler

@app.login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates a user to facebook
    """
    return app.fb.authorize(callback='http://sniffio.com:5000'+url_for('fbcheck'))

@app.route('/logout')
def logout():
    """
    Logs a user out, regirects to index
    """
    if current_user.is_authenticated():
        logout_user()
    return redirect("/")

@app.route('/fbcheck')
@app.fb.authorized_handler
def fbcheck(resp):
    """
    Checks for facebook authentication, stores the user and the user's pages, if he has any
    """
    if resp is None:
        # The authentication failed.
        return redirect("/")

    session['oauth_token'] = (resp['access_token'], '')
    me = app.fb.get('/me')
    user = User.query.filter_by(fb_id=me.data['id']).first()
    if not user:
        #Add new user
        user = User(fb_id=me.data['id'], fb_data=json.dumps(me.data))
        app.db.session.add(user)
    else:
        user.fb_data=json.dumps(me.data)
    # Commit user object
    app.db.session.commit()

    # Get user pages and add them as services to DB
    pages = app.fb.get('/'+me.data['id']+'/accounts')
    for fservice in pages.data['data']:
        service = Service.query.filter_by(fb_id=fservice['id']).first()
        if not service:
            # Add service
            service = Service(fb_id=fservice['id'],
                              cat_id=1, #hardcode, to remove
                              name=fservice['name'],
                              fb_category=fservice['category'],
                              fb_access_token=fservice['access_token'])
            app.db.session.add(service)
            # TODO: Need to optimize - store services in dict and commit once, then get the populated service ids
            # and commit adminservices in the end
            app.db.session.commit()
        else:
            # TODO: Update service if needed, especially access token, may need to store expiration date
            pass
        # Add service to user's admined services
        asv = AdminServices(service_id=service.id, user_id=user.id,
                            permissions=json.dumps(fservice['perms']))
        db.session.add(asv)

    app.db.session.commit()
    login_user(user)
    return redirect("/")

@app.route('/')
def index():
    """
    Serves the index file
    """
    resp = make_response(render_template('index.html'))
    return resp

@app.fb.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

# TODO: Need to find a way to remove duplicate code.
app.api_manager.create_api(User,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(User, **kw)],
                                              GET_MANY=[lambda **kw: handler(User, **kw)]),
                           methods=['GET', 'POST'], url_prefix='/api/my')


app.api_manager.create_api(Action,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Action, **kw)],
                                              GET_MANY=[lambda **kw: handler(Action, **kw)]),
                           methods=['GET', 'POST'])

app.api_manager.create_api(Service,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Service, **kw)],
                                              GET_MANY=[lambda **kw: handler(Service, **kw)]),
                           methods=['GET'],
                           exclude_columns=['fb_access_token','admins'])

app.api_manager.create_api(Service,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Service, my=True, **kw)],
                                              GET_MANY=[lambda **kw: handler(Service, my=True, **kw)]),
                           postprocessors=dict(GET_SINGLE=[lambda **kw: post_handler(Service, my=True, **kw)],
                                              GET_MANY=[lambda **kw: post_handler(Service, my=True, **kw)]),
                           methods=['GET', 'POST'], url_prefix='/api/my')

app.api_manager.create_api(Category,
                           preprocessors=dict(GET_SINGLE=[lambda **kw: handler(Category, **kw)],
                                              GET_MANY=[lambda **kw: handler(Category, **kw)]),
                           methods=['GET', 'POST'])
