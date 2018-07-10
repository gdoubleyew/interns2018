import flask
from flask import Flask, request  # , send_file
import argparse
import pickle
import time
import threading
import random
# import base64
# import io

app = Flask(__name__)

finished = False
# http://localhost:5200/
def work():
    global finished
    num = random.randint(1,3)
    time.sleep(num)
    finished = True

@app.route('/calcDelta', methods=['GET', 'POST'])
def calcDelta():
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
        client_ts = float(request.args['client_ts'])
        server_ts = time.time()

        returnValue = {
            "request_id": request_id,
            "client_ts": client_ts,
            "server_ts": server_ts,
            #"Delta_here": Delta_here
        }


        rv = flask.make_response(flask.jsonify(returnValue), 400)
        return rv

    else:
        return '''
        <html><body><h1>hi!</h1></body></html>
        '''


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
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

        # request_id = request.args['request_id']
        #
        # returnValue = {
        #     "request_id": request_id,
        #     "client_ts": client_ts,
        #     "server_ts": server_ts,
        #     #"Delta_here": Delta_here


        # }
        client_ts = float(request.args['client_ts'])
        server_ts = time.time()
        delta = float(request.args['delta'])
        hTT = server_ts - client_ts
        dedline = 2 - ((2*hTT)+delta)

        workT = threading.Thread(target=work)
        workT.start()
        workT.join(timeout=dedline)
        if finished == True:
            returnValue= {"return": "succses"}
        else:
            returnValue= {"return": "failed"}


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
