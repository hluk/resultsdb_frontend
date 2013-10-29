# This is required for running on EL6
#import __main__
#__main__.__requires__ = ['SQLAlchemy >= 0.7', 'Flask >= 0.9', 'jinja2 >= 2.6']
#import pkg_resources

activate_this = '/var/www/resultsdb_frontend/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0,"/var/www/resultsdb_frontend/")

from resultsdb_frontend import app as application
