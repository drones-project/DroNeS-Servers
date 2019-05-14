import json
from flask import Flask, jsonify, request, abort
from Routing.Pathfinder import SmartPathfinder
from Scheduling.Scheduler import FCFSScheduler

app = Flask(__name__)

# run the scheduler
scheduler = FCFSScheduler()
scheduler.start()

# create a pathfinder
pathfinder = SmartPathfinder()


@app.route('/')
def home():
    return "This is the root directory of the web server."


@app.route('/routes', methods=['GET', 'POST'])
def routes():
    global written
    if request.method == 'POST':
        data = request.get_json()
        return pathfinder.getRoute(data), 200
    elif request.method == 'GET':
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        data = request.get_json()
        return scheduler.getJob(data), 200
    elif request.method == 'GET':
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


@app.route('/update_timescale', methods=['POST'])
def update_timescale():
    if request.is_json:
        data = request.get_json()
        app.logger.debug(json.dumps(data))
        scheduler.updateTimescale(data['timescale'])
        return jsonify({'success': 'true'}), 200
    else:
        return abort(400)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
