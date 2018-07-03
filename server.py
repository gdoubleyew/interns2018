import flask
from flask import Flask, request  # , send_file
import argparse
import pickle
import time
# import base64
# import io

app = Flask(__name__)

# http://localhost:5200/

@app.route('/', methods=['GET', 'POST'])
def index():
    """TODO (dsuo): Add comments.

    TODO (dsuo): Maybe care about batching
    TODO (dsuo): REST is nice conceptually, but probably too much overhead
    TODO (dsuo): Move logic to C++ (keep as head node process)

    NOTE: We do an extra serialize during get and extra deserialize during
        put.
    """
    if request.method == 'POST':
        request_id = request.files['request_id'].read()
        data = request.files['value'].read()
        value = pickle.loads(data)
        print("POST: {}".format(value))
        # TODO - do something with value

        return request_id

    elif request.method == 'GET':
        request_id = request.args['request_id']
        client_ts = request.args['client_ts']
        server_ts = time.time()

        returnValue = {
            "request_id": request_id,
            "client_ts": client_ts,
            "server_ts": server_ts
        }

        rv = flask.make_response(flask.jsonify(returnValue), 400)
        return rv

    else:
        return '''
        <html><body><h1>hi!</h1></body></html>
        '''


def main():
    parser = argparse.ArgumentParser(description="Realtime Server")
    parser.add_argument('-p', action="store", dest="port")
    args = parser.parse_args()

    app.run(host="0.0.0.0", debug=False, port=args.port)


if __name__ == '__main__':
    main()
