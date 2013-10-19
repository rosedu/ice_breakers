__author__ = 'Radu'

import os
import sys
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, dirname)

from crossco import app
import crossco.routes

app.run()

