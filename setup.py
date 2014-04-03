from setuptools import setup

setup(name='resultsdb_frontend',
      version='1.0.0',
      description='Frontend for the ResultsDB',
      author='Josef Skladanka',
      author_email='jskladan@redhat.com',
      license='GPLv2+',
      packages=['resultsdb_frontend', 'resultsdb_frontend.controllers', 'resultsdb_frontend.models'],
      package_dir={'resultsdb_frontend':'resultsdb_frontend'},
      entry_points=dict(console_scripts=['resultsdb_frontend=resultsdb_frontend.cli:main']),
      include_package_data=True,
     )
