__author__ = 'Radu'

from flask.ext.login import current_user
from flask.ext.restless import ProcessingException
from crossco.models.models import *

def handler(model, **kw):
    if not current_user.is_authenticated():
        raise ProcessingException(message='Not authenticated!')


    if 'instance_id' not in kw:
        #get all users corresponding to me
        if 'filters' not in kw['search_params']:
            kw['search_params']['filters'] = []
        if model == User:
            kw['search_params']['filters'].append({u'name': u'id', u'val': current_user.id, u'op': u'eq'});
        elif model == Action:
            kw['search_params']['filters'].append({u'name': u'user_id', u'val': current_user.id, u'op': u'eq'});
 

    elif kw['instance_id'] != str(current_user.id):
        raise ProcessingException(message='Unauthorized!')

