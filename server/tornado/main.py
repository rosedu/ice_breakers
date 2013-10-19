__author__ = 'Radu'

import sys
import tornado.ioloop
import tornado.web

import pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get

web_app_path = './webapp'

#sys.path.append('')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open(web_app_path+'/index.html') as f:
            self.write(f.read())

class APIService(pyrestful.rest.RestHandler):
      @get(_path="/api/{model}/{id}", _produces=mediatypes.APPLICATION_JSON)
      def loadModel(self, model, id):
           return {"Hello":model}


application = pyrestful.rest.RestService([APIService],
    handlers=[(r"/", IndexHandler),
              (r"/webapp/(.*)",tornado.web.StaticFileHandler, {"path": web_app_path},)],
    debug=True)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
