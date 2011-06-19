#
#  GigaPan Mobile
#
#  Version: MPL 1.1/GPL 3/LGPL 3
#
#  The contents of this file are subject to the Mozilla Public License Version
#  1.1 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at
#  http://www.mozilla.org/MPL/
#
#  Software distributed under the License is distributed on an "AS IS" basis,
#  WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
#  for the specific language governing rights and limitations under the
#  License.
#
#  The Original Code is the GigaPan Mobile.
#
#  The Initial Developer of the Original Code is Daniel Gasienica.
#  Portions created by the Initial Developer are Copyright (c) 2007-2009
#  the Initial Developer. All Rights Reserved.
#
#  Contributor(s):
#    Daniel Gasienica <daniel@gasienica.ch>
#
#  Alternatively, the contents of this file may be used under the terms of
#  either the GNU General Public License Version 3 or later (the "GPL"), or
#  the GNU Lesser General Public License Version 3 or later (the "LGPL"),
#  in which case the provisions of the GPL or the LGPL are applicable instead
#  of those above. If you wish to allow use of your version of this file only
#  under the terms of either the GPL or the LGPL, and not to allow others to
#  use your version of this file under the terms of the MPL, indicate your
#  decision by deleting the provisions above and replace them with the notice
#  and other provisions required by the GPL or the LGPL. If you do not delete
#  the provisions above, a recipient may use your version of this file under
#  the terms of any one of the MPL, the GPL or the LGPL.
#


from google.appengine.api.urlfetch import fetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import logging
import simplejson as json

from models import GigaPan, GigaPanUser

# Constants
DEFAULT_RESULT_COUNT = 100
MAX_RESULT_COUNT = 500


# Handlers
class SearchRequestHandler(webapp.RequestHandler):
    def get(self):
        q = self.request.get("q")
        self.response.out.write(q)


class SimpleQueryRequestHandler(webapp.RequestHandler):
    def get(self, query='SELECT * FROM GigaPan ORDER BY id DESC'):
        count = get_count(self.request)
        gigapans = get_gigapans(query, count)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(gigapans))

class PopularRequestHandler(SimpleQueryRequestHandler):
    def get(self):
        query = 'SELECT * FROM GigaPan ORDER BY explore_score DESC'
        super(PopularRequestHandler, self).get(query)

class RecentRequestHandler(SimpleQueryRequestHandler):
    def get(self):
        query = 'SELECT * FROM GigaPan ORDER BY id DESC'
        super(RecentRequestHandler, self).get(query)


# Functions
def get_gigapans(query, count):
    models = db.GqlQuery(query).fetch(count)
    gigapans = []
    for model in models:
        gigapan = {
            'id': model.id,
            'name': model.name,
            'width': model.width,
            'height': model.height
        }
        gigapans.append(gigapan)
    return gigapans

def get_count(request):
    return min(int(request.get('count', DEFAULT_RESULT_COUNT)), MAX_RESULT_COUNT)


# Application
application = webapp.WSGIApplication([
    ('/api/1/search', SearchRequestHandler),
    ('/api/1/recent', RecentRequestHandler),
    ('/api/1/popular', PopularRequestHandler),
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
