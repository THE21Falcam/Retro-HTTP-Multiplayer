from flask import Flask, Response, request
import time
import json

app = Flask(__name__)

client_connected = {}

@app.route("/")
def index():
    return "SSE HOST"

@app.route("/playmove", methods=['POST'])
def playmove():
    data = request.get_json()
    client_connected[str(data['data'][0])] = [int(data['data'][1]), int(data['data'][2])]
    return "Movement Handle"

@app.route('/stream', methods=['GET'])
def stream():
    user = request.headers.get('Authorization')
    if user == "Hello":
        return "Sorry"
    def event_stream():
        try:
            while True:
                time.sleep(1/3)
                yield f"{json.dumps(client_connected)}\n"
        finally:
            del client_connected[user]
            print(user , " Disconnected")

    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers['X-Accel-Buffering'] = 'no'
    return response

if __name__ == '__main__':
        app.run(threaded=True)
        app.run(debug=True)
