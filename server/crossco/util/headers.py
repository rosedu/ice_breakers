__author__ = 'Radu'

def add_cors_header(response):
    allow = 'GET, HEAD, OPTIONS'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = allow
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    #response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response