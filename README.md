# ResultsDB frontend

ResultsDB fronted is a simple application that allows browsing the data stored inside ResultsDB.

## Repositories

* ResultsDB - [Bitbucket GIT repo](https://bitbucket.org/rajcze/resultsdb)
* ResultsDB Client Library - [Bitbucket GIT repo](https://bitbucket.org/rajcze/resultsdb_api)

## Hacking

You'll need to stand up an instance of the core
[resultsdb](https://bitbucket.org/rajcze/resultsdb) alongside this frontend for
it to work.

First, clone the repository.

Then, setup a virtual environment for development.

    $ sudo yum install python-virtualenv
    $ virtualenv resultsdb_frontend
    $ source resultsdb_frontend/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py install

Setup a config file:

    $ cp conf/settings.py.example conf/settings.py
    $ # edit conf/settings.py accordingly

Initialize your database:

    $ ./init_db.sh

Run the server

    $ python runapp.py
