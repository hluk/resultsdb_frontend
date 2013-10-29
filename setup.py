from setuptools import setup

setup(name='resultsdb_frontend',
      version='0.0.1',
      description='',
      author='',
      author_email='',
      license='GPLv2+',
      packages=['resultsdb_frontend', 'resultsdb_frontend.controllers', 'resultsdb_frontend.models'],
      package_dir={'resultsdb_frontend':'resultsdb_frontend'},
      entry_points=dict(console_scripts=['resultsdb_frontend=resultsdb_frontend.cli:main']),
      include_package_data=True,
      install_requires = [
        'Flask==0.9',
        'Flask-SQLAlchemy==0.16',
        'SQLAlchemy>= 0.7',
        'MySQL-python >= 1.2.0',
        'WTForms>1.0',
        'Flask-WTF==0.8',
        'Flask-Login>=0.1.3',
        'resultsdb_api',
     ]
     )


#FIXME: change Flask-WTF to >= 0.8 (?) there seems to be a bug now (see below), or it might be connected to the Flask version - find out!
# File "/home/jskladan/flask_virtualenv/lib/python2.7/site-packages/Flask_WTF-0.9.0-py2.7.egg/flask_wtf/recaptcha/widgets.py", line 5, in <module>
#     from flask.json import dumps, JSONEncoder
