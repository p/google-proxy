# -*- coding: utf-8 -*-

import webracer
import webracer.utils.runwsgi
import bapp

setup_module, teardown_module = \
    webracer.utils.runwsgi.app_runner_setup((bapp.app, 8050))

@webracer.config(host='localhost', port=8050)
class RequestTest(webracer.WebTestCase):
    def test_request(self):
        self.get('/')
        self.assert_status(200)
    
    def test_unicode_query(self):
        self.get('/search', dict(q='Don’t'))
        self.assert_status(200)
