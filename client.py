import requests
import pickle
import argparse
import time
import os
# import subprocess


# client to run analysis
class Client(object):
    """A class to communicate with a REST server.
    """

    def __init__(self,
                 gateway_address,
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

    if client is None:
        print("No client spesified")
        quit()
    # if no file is entered (make default file name)
    if not isinstance(file, str):
        file = "Default.txt"
    # reset defaulting to true
    if not isinstance(reset, bool):
        reset = True
    # opens file with perditermined clock diffrence
    if not reset:
        if os.path. exists(file):
            with open(file, "r") as Dfile:
                clockSkew = Dfile.read()
    # test_offset defaults to 0
    if not isinstance(test_offset, float) and not isinstance(test_offset, int):
        test_offset = 0
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

            a = server_ts - client_ts       # I think this formula is causing an error
            b = server_ts - client_ts2      #
            RTT = a - b
            clockSkew = (a + b)/2

            RTT_list.append(RTT)
            clockSkew_list.append(clockSkew)
        RTT = min(RTT_list)
        clockSkew = clockSkew_list[RTT_list.index(RTT)]

        if file is not None:
            with open(file, "w+") as Dfile:
                Dfile.write("{}".format(clockSkew))
        # deleting default file
        if os.path.exists("Default.txt"):
            os.remove("Default.txt")

    return clockSkew


def analysis(client, clockSkew_file=None, work_diff=0):
    clockSkew = None

    if client is None:
        print("No client spesified")
        quit()
    # if no file is entered (it creat a temperary file)
    if clockSkew_file is None:
        with open("Default.txt", "w+") as Dfile:
            Dfile.close()
        with open("Default.txt", "r") as Dfile:
            clockSkew = Dfile.read()
            Dfile.close()
            print("Please enter a file next time round.")
    # cheaking work difficulty is usable
    if isinstance(work_diff, float) or isinstance(work_diff, int):
        # to make sure there are no negatives
        work_diff = abs(work_diff)
    else:
        work_diff = 0

        # check if ClockSkew is in file
    if not clockSkew:
        clockSkew = calcClockSkew(client, clockSkew_file, True)
    # returnVals = [] #for testing
    # succsesful = [] #for testing
    # deadline_list = []
    client_ts = time.time()
    deadline = client_ts + 2 - float(clockSkew)
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
    time_took = final_ts - client_ts  # for testing
    # succsesful.append(vals['return']) #for testing
    # returnVals.append(time_took) #for testing
    # deadline_list.append(deadline) #for testing
    return (vals['return'], time_took, vals['deadline'])  # for testing
    if os.path.exists("Default.txt"):
        os.remove("Default.txt")


def main():
    parser = argparse.ArgumentParser(description="Realtime Client")
    parser.add_argument('-a', action="store", dest="addr", default="localhost")
    parser.add_argument('-p', action="store", dest="port", default=5200)
    # parser.add_argument('-r', action="store", default = False)
    args = parser.parse_args()

    # creates client object
    client = Client(args.addr, args.port)

    calcClockSkew(client, "clockSkew_file.txt", True, "1,2,2")
    analysis(client, "clockSkew_file.txt", 2)


if __name__ == "__main__":
    main()
