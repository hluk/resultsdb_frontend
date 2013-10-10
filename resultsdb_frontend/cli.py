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

# This is required for running on EL6
import __main__
__main__.__requires__ = ['SQLAlchemy >= 0.7', 'Flask >= 0.9', 'jinja2 >= 2.6']
import pkg_resources


from optparse import OptionParser
import sys

from resultsdb_frontend import db
from resultsdb_frontend.models.user import User


def initialize_db():
    print "Initializing Database"
    db.drop_all()
    db.create_all()

def mock_data():
    data = [('admin', 'admin'), ('user', 'user')]

    for d in data:
        u = User(*d)
        db.session.add(u)
    db.session.commit()



if __name__ == '__main__':

    possible_commands = ['init_db', 'mock_data']

    usage = 'usage: [DEV=true] %prog ' + "(%s)" % ' | '.join(possible_commands)
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) < 1:
        print usage
        print
        print 'Please use one of the following commands: %s' % str(possible_commands)
        sys.exit(1)


    command = args[0]
    if not command in possible_commands:
        print 'Invalid command: %s' % command
        print 'Please use one of the following commands: %s' % str(possible_commands)
        sys.exit(1)


    if command == 'init_db':
        initialize_db()
    elif command == 'mock_data':
        mock_data()

    sys.exit(0)
