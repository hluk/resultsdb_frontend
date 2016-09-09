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

from resultsdb_api import ResultsDBapi, ResultsDBapiException

rdb_api = None


main = Blueprint('main', __name__)

@app.before_first_request
def before_first_request():
    global rdb_api
    rdb_api = ResultsDBapi(app.config['RDB_URL'])

@main.route('/')
@main.route('/index')
def index():
     return redirect(url_for('main.results'))

@main.route('/groups')
def groups():
    groups = rdb_api.get_groups(**dict(request.args))
    return render_template('groups.html', groups = groups)

@main.route('/groups/<group_id>')
def group(group_id):
    try:
        group = rdb_api.get_groups(group_id)
    except ResultsDBapiException as e:
        return str(e)
    groups = dict(prev = None, next = None, data = [group])
    return render_template('groups.html', groups = groups)

@main.route('/results')
def results():
    args = dict(request.args)
    results = rdb_api.get_results(**args)
    for result in results['data']:
        result['groups'] = (len(result['groups']), ','.join([r.split('/')[-1].strip() for r in result['groups']]))
    return render_template('results.html', results = results)

@main.route('/results/<result_id>')
def result(result_id):
    try:
        result = rdb_api.get_result(id = result_id)
    except ResultsDBapiException as e:
        return str(e)
    result['groups'] = (len(result['groups']), ','.join([r.split('/')[-1].strip() for r in result['groups']]))
    return render_template('result_detail.html', result = result)

@main.route('/testcases')
def testcases():
    args = dict(request.args)
    tcs = rdb_api.get_testcases(**args)
    return render_template('testcases.html', testcases = tcs)

@main.route('/testcases/<testcase_name>')
def testcase(testcase_name):
    try:
        tc = rdb_api.get_testcase(name = testcase_name)
    except ResultsDBapiException as e:
        return str(e)
    tcs = dict(prev = None, next = None, data = [tc])
    return render_template('testcases.html', testcases = tcs)

