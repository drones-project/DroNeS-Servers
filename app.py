import json

from flask import Flask, jsonify, request, abort
from Routing.Pathfinder import Pathfinder
from Scheduling.Scheduler import FCFSScheduler

app = Flask(__name__)

# run the scheduler
s = FCFSScheduler()
s.start()

@app.route('/')
def home():
    return "This is the root directory of the web server."


@app.route('/routes', methods=['POST'])
def routes():
    if request.is_json:
        app.logger.info(json.dumps(request.json))
        r = Pathfinder.getRoutes(request.json)
        return jsonify(r)
    else:
        return abort(400)


@app.route('/jobs', methods=['POST'])
def jobs():
    if request.is_json:
        app.logger.info(json.dumps(request.json))
        return s.getJob(1)
    else:
        return abort(400)


@app.route('/jobs_dummy')
def jobs_dummy():
    return s.getJob(1)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
