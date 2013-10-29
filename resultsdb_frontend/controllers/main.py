# Copyright 2013, Red Hat, Inc
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
#   Josef Skladanka <jskladan@redhat.com>

from flask import Blueprint, render_template, redirect, url_for, request
from resultsdb_frontend import app

from resultsdb_api import ResultsDBapi

RDB_URL = 'http://localhost:5000/api/v1.0'
rdb_api = None


main = Blueprint('main', __name__)

@app.before_first_request
def before_first_request():
    global rdb_api
    rdb_api = ResultsDBapi(RDB_URL)

@main.route('/')
@main.route('/index')
def index():
     return redirect(url_for('main.jobs'))

@main.route('/jobs')
def jobs():
    jobs = rdb_api.get_jobs(**dict(request.args))
    return render_template('jobs.html', jobs = jobs)

@main.route('/jobs/<job_id>')
def job(job_id):
    job = rdb_api.get_job(id = job_id)
    jobs = dict(prev = None, next = None, data = [job])
    return render_template('jobs.html', jobs = jobs)

@main.route('/results')
def results():
    args = dict(request.args)
    if 'job_id' in args:
        args['job_id'] = request.args['job_id']
    results = rdb_api.get_results(**args)
    return render_template('results.html', results = results)

@main.route('/results/<result_id>')
def result(result_id):
    result = rdb_api.get_result(id = result_id)
    return render_template('result_detail.html', result = result)

@main.route('/testcases')
def testcases():
    args = dict(request.args)
    tcs = rdb_api.get_testcases(**args)
    return render_template('testcases.html', testcases = tcs)

@main.route('/testcases/<testcase_name>')
def testcase(testcase_name):
    tc = rdb_api.get_testcase(name = testcase_name)
    tcs = dict(prev = None, next = None, data = [tc])
    return render_template('testcases.html', testcases = tcs)

