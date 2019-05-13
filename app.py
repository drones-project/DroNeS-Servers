import json
from flask import Flask, jsonify, request, abort
from Routing.Pathfinder import DumbPathfinder
from Scheduling.Scheduler import FCFSScheduler

app = Flask(__name__)

# run the scheduler
scheduler = FCFSScheduler()
scheduler.updateTimescale(1)
scheduler.start()

# create a pathfinder
pathfinder = DumbPathfinder()

written = False


@app.route('/')
def home():
    return "This is the root directory of the web server."


@app.route('/routes', methods=['GET', 'POST'])
def routes():
    global written
    if request.method == 'POST':
        app.logger.info(json.dumps(request.get_json()))
        return pathfinder.getRoute(request.get_json()), 200
    elif request.method == 'GET':
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        data = request.get_json()
        # app.logger.info(json.dumps(data))
        job = scheduler.getJob(data)
        app.logger.info("Giving job...")
        app.logger.info(job)
        app.logger.info("")
        return job, 200
    elif request.method == 'GET':
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


@app.route('/update_timescale', methods=['POST'])
def update_timescale():
    if request.is_json:
        app.logger.debug(json.dumps(request.json))
        scheduler.updateTimescale(int(request.json['timescale']))
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
