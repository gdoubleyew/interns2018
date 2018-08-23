import requests
import pickle
import argparse
import time
import os
from serial import Serial
from random import randint
# import subprocess


# client to run analysis
class Client(object):
    """A class to communicate with a REST server.
    """

    def __init__(self,
                 gateway_address="localhost",
                 gateway_port=5200):
        """Initialize a new client.

        Args:
            gateway_address (str): The IP address of the head node / gateway.
            gateway_port (int): The gateway's port.

        Returns:
            A new Client object
        """
        self.gateway_address = gateway_address
        self.gateway_port = gateway_port
        self.url = "http://{}:{}".format(
            self.gateway_address,
            self.gateway_port)

    def put(self, url_P2, request_id, value):
        data = pickle.dumps(value)
        res = requests.post(url=self.url + '/' + url_P2,
                            files={
                                "value": data,
                                "request_id": request_id
                            })
        return res

    def get(self, url_P2, params):
        res = requests.get(url=self.url + '/' + url_P2, params=params)
        # objects = self.serialization_context.deserialize(res.raw.read())
        return res


def calcClockSkew(client, file=None, reset=True, test_offset=0):
    clockSkew = None
    max_RTT = None

    if client is None:
        raise ValueError("No client spesified")
    # opens file with perditermined clock diffrence
    if not reset:
        if os.path.exists(file):
            with open(file, "r") as Dfile:
                clockSkew = float(Dfile.readline())
                max_RTT = float(Dfile.readline())
            # print("Clock Skew: {}".format(clockSkew))
            # print("RTT: {}".format(max_RTT))
    # recalculate ClockSkew if needed
    if not clockSkew:
        RTT_list = []
        clockSkew_list = []
        for i in range(100):
            client_ts = time.time()
            params = {
                "request_id": 1,
                "client_ts": client_ts,
                "test_offset": test_offset
            }
            res = client.get("calcClockSkew", params)
            vals = res.json()
            client_ts2 = time.time()
            server_ts = vals['server_ts']

            a = server_ts - client_ts       # Refrence paper
            b = server_ts - client_ts2      #
            RTT = a - b
            clockSkew = (a + b)/2

            RTT_list.append(RTT)
            clockSkew_list.append(clockSkew)
        min_RTT = min(RTT_list)
        max_RTT = max(RTT_list)
        clockSkew = clockSkew_list[RTT_list.index(min_RTT)]

        if file is not None:
            with open(file, "w+") as Dfile:
                Dfile.write("{}\n".format(clockSkew))
                Dfile.write("{}".format(max_RTT))

    return clockSkew, max_RTT


def analysis(client, clockSkew_file=None, work_diff=0):

    if work_diff < 0:
        work_diff = 0

    clockSkew, max_RTT = calcClockSkew(client, clockSkew_file, False)

    client_ts = time.time()
    deadline = client_ts + 2 + float(clockSkew) - max_RTT  # test if this should add clock skew
    params = {
        "request_id": 1,
        "client_ts": client_ts,
        "deadline": deadline,
        "work_diff": work_diff
    }
    res = client.get("analysis", params)
    vals = res.json()
    final_ts = time.time()  # for testing
    print(vals['return'])
    print("deadline: {}".format(vals['deadline']))
    time_took = final_ts - client_ts  # for testing
    # succsesful.append(vals['return']) #for testing
    # returnVals.append(time_took) #for testing
    # deadline_list.append(deadline) #for testing
    return (vals['return'], time_took, vals['deadline'])  # for testing


def main():
    parser = argparse.ArgumentParser(description="Realtime Client")
    parser.add_argument('-a', action="store", dest="addr", default="localhost")
    parser.add_argument('-p', action="store", dest="port", default=5200)
    # parser.add_argument('-r', action="store", default = False)
    args = parser.parse_args()

    # creates client object
    client = Client(args.addr, args.port)

    calcClockSkew(client, "clockSkew_file.txt", True)

    ser = Serial('/dev/ttyUSB0', 9600)
    for i in range(10):
        response = ser.read()
        val = response.decode("utf-8")
        val = int(val)
        assert 0 <= val <= 9
        ran = randint(0, 3)
        print(ran)
        analysis(client, "clockSkew_file.txt", ran)
    ser.close()


if __name__ == "__main__":
    main()
