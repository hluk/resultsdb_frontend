from setuptools import setup

setup(name='resultsdb_frontend',
      version='1.0.0',
      description='Frontend for the ResultsDB',
      author='Josef Skladanka',
      author_email='jskladan@redhat.com',
      license='GPLv2+',
      packages=['resultsdb_frontend', 'resultsdb_frontend.controllers'],
      package_dir={'resultsdb_frontend':'resultsdb_frontend'},
      include_package_data=True,
     )
