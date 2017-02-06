# ResultsDB frontend

ResultsDB fronted is a simple application that allows browsing the data stored inside ResultsDB.

## Repositories

* ResultsDB - [GIT repo](https://pagure.io/taskotron/resultsdb)
* ResultsDB Client Library - [GIT repo](https://pagure.io/taskotron/resultsdb_api)

## Quick development setup

You'll need to stand up an instance of the core
[resultsdb](https://pagure.io/taskotron/resultsdb) alongside this frontend
for it to work.

First, clone the repository.

Then, setup a virtual environment for development:

    $ sudo dnf install python-virtualenv
    $ virtualenv env_resultsdb_frontend
    $ source env_resultsdb_frontend/bin/activate
    $ pip install -r requirements.txt

Run the server:

    $ DEV=true python runapp.py

The ResultsDB frontend is now running at <http://localhost:5002>. It expects
the ResultsDB server to be available at <http://localhost:5001/api/v2.0>.

## Adjusting configuration

You can configure this app by copying `conf/settings.py.example` into
`conf/setting.py` and adjusting values as you see fit. It overrides default
values in `resultsdb_frontend/config.py`.

## Using with libtaskotron

You might want to use this tool together with libtaskotron. To use your own
*ResultsDB frontend* in libtaskotron, edit `/etc/taskotron/taskotron.yaml` and
set the following value::

    resultsdb_frontend: http://localhost:5002
