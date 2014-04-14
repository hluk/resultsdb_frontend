from setuptools import setup
import codecs
import re
import os

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='resultsdb_frontend',
      version=find_version('resultsdb_frontend', '__init__.py'),
      description='Frontend for the ResultsDB',
      author='Josef Skladanka',
      author_email='jskladan@redhat.com',
      license='GPLv2+',
      packages=['resultsdb_frontend', 'resultsdb_frontend.controllers'],
      package_dir={'resultsdb_frontend':'resultsdb_frontend'},
      include_package_data=True,
     )
