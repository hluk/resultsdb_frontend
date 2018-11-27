# Copyright 2013-2014, Red Hat, Inc
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors:
#   Tim Flink <tflink@redhat.com>
#   Josef Skladanka <jskladan@redhat.com>
#   Ralph Bean <rbean@redhat.com>


from flask import Flask, render_template
from resultsdb_frontend import proxy

import logging
import logging.handlers
import os

# the version as used in setup.py
__version__ = "2.1.0"

# Flask App
app = Flask(__name__)
app.secret_key = 'replace-me-with-something-random'

app.wsgi_app = proxy.ReverseProxied(app.wsgi_app)

# Expose the __version__ variable in templates
app.jinja_env.globals['app_version'] = __version__

# Load default config, then override that with a config file
if os.getenv('DEV') == 'true':
    default_config_obj = 'resultsdb_frontend.config.DevelopmentConfig'
    default_config_file = os.getcwd() + '/conf/settings.py'
elif os.getenv('TEST') == 'true':
    default_config_obj = 'resultsdb_frontend.config.TestingConfig'
    default_config_file = os.getcwd() + '/conf/settings.py'
else:
    default_config_obj = 'resultsdb_frontend.config.ProductionConfig'
    default_config_file = '/etc/resultsdb_frontend/settings.py'

app.config.from_object(default_config_obj)

config_file = os.environ.get('RESULTSDB_FRONTEND_CONFIG', default_config_file)

if os.path.exists(config_file):
    app.config.from_pyfile(config_file)

if app.config['PRODUCTION']:
    if app.secret_key == 'replace-me-with-something-random':
        raise Warning("You need to change the app.secret_key value for production")

# setup logging
fmt = '[%(filename)s:%(lineno)d] ' if app.debug else '%(module)-12s '
fmt += '%(asctime)s %(levelname)-7s %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
loglevel = logging.DEBUG if app.debug else logging.INFO
formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

def setup_logging():
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)

    if app.config['STREAM_LOGGING']:
        print("doing stream logging")
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)
        app.logger.addHandler(stream_handler)

    if app.config['SYSLOG_LOGGING']:
        print("doing syslog logging")
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log',
                            facility=logging.handlers.SysLogHandler.LOG_LOCAL4)
        syslog_handler.setLevel(loglevel)
        syslog_handler.setFormatter(formatter)
        root_logger.addHandler(syslog_handler)
        app.logger.addHandler(syslog_handler)

    if app.config['FILE_LOGGING'] and app.config['LOGFILE']:
        print("doing file logging to %s" % app.config['LOGFILE'])
        file_handler = logging.handlers.RotatingFileHandler(app.config['LOGFILE'], maxBytes=500000, backupCount=5)
        file_handler.setLevel(loglevel)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        app.logger.addHandler(file_handler)

setup_logging()

# register blueprints
from resultsdb_frontend.controllers.main import main
app.register_blueprint(main)
