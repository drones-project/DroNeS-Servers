import json
import os
import unittest
from app import app
from jsonschema import validate


def load_schema(filename):
    file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
    with open(file) as f:
        return json.loads(f.read())


class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def terminate(self, app):
        app.post("/update_timescale",
                 data=json.dumps({'timescale': 0}),
                 content_type='application/json')

    def testRootDirectoryExists(self):
        rv = self.app.get("/")
        assert(b'This is the root directory of the web server.' in rv.data)
        return

    def testGetEndpointsReturn200(self):
        rv = self.app.get("/jobs")
        assert(rv.json['success'])
        rv = self.app.get("/routes")
        assert(rv.json['success'])
        rv = self.app.get("/update_timescale")
        assert(rv.json['success'])
        return

    def testMalformedPostEndpointsReturn400(self):
        rv = self.app.post("/jobs")
        assert(rv.status_code == 400)
        rv = self.app.post("/routes")
        assert(rv.status_code == 400)
        rv = self.app.post("/update_timescale")
        assert(rv.status_code == 400)
        return

    def testRoutesEndpoint(self):
        rv = self.app.post("/routes",
                           data="{}",
                           content_type='application/json')
        assert(rv.status_code == 200)
        validate(eval(rv.data), load_schema('route.json'))
        return

    def testJobEndpoint(self):
        rv = self.app.post("/jobs",
                           data="{}",
                           content_type='application/json')
        assert(rv.status_code == 200)
        assert(rv.data == b'{}')
        return

    def testUpdateTimescaleEndpoint(self):
        rv = self.app.post("/update_timescale",
                           data=json.dumps({'timescale': 5}),
                           content_type='application/json')
        assert(rv.status_code == 200)
        assert(rv.json['success'])
        assert(rv.json['timescale'] == 5)
        # to terminate the scheduling thread
        self.terminate(self.app)
        return


if __name__ == "__main__":
    unittest.main()
