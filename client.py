import requests
import pickle
import argparse
import time
import random
# import subprocess

#client to run analasis
class AClient(object):
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

    def put(self, request_id, value):
        data = pickle.dumps(value)
        res = requests.post(url=self.url + '/' + "analysis",
                            files={
                                "value": data,
                                "request_id": request_id
                            })
        return res

    def get(self, params):
        res = requests.get(url=self.url + '/' + "analysis", params=params)
        # objects = self.serialization_context.deserialize(res.raw.read())
        return res

#client to calculate Delta
class DClient(object):
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

    def put(self, request_id, value):
        data = pickle.dumps(value)
        res = requests.post(url=self.url + '/' + "calcDelta",
                            files={
                                "value": data,
                                "request_id": request_id
                            })
        return res

    def get(self, params):
        res = requests.get(url=self.url + '/' + "calcDelta", params=params)
        # objects = self.serialization_context.deserialize(res.raw.read())
        return res


def main():
    parser = argparse.ArgumentParser(description="Realtime Client")
    parser.add_argument('-a', action="store", dest="addr", default="localhost")
    parser.add_argument('-p', action="store", dest="port", default=5200)
    #parser.add_argument('-r', action="store", default = False)
    args = parser.parse_args()

    #opens file were Delta is (or is not)
    Dfile = open("Delta_file.txt", "r+")
    Delta = Dfile.read()
    print(Delta)
    #checks to see if delta is in file and skips this block if it is
    if not Delta:
        DClient = DClient(args.addr, args.port)
        rtt_list = []
        total = []
        for i in range(0,100):
            client_ts = time.time()
            params = {
            "request_id": 1,
            "client_ts": client_ts
            }
            res = DCient.get(params)
            client_ts2 = time.time()
            vals = res.json()
            server_ts = vals['server_ts']

            rtt = client_ts2 - client_ts
            rtt_list.append(rtt)

            TT = rtt/2
            D = client_ts2 - server_ts - TT
            total.append(D)
        #calculates delta and writes it to Dfile
        min_T = min(rtt_list)
        best_val = total[rtt_list.index(min_T)]
        print("Total: {}".format(best_val))
        Dfile.close()
        Dfile = open("Delta_file.txt", "w+")
        Dfile.write("{}".format(best_val))

    Client = AClient(args.addr, args.port)

    client_ts = time.time()
    work_diff = random.randint(1, 3)
    dedline = client_ts + 2 + float(Delta)
    params = {
    "request_id": 1,
    "client_ts": client_ts,
    "dedline": dedline,
    "work_diff": work_diff
    }
    res = Client.get(params)
    vals = res.json()
    print(vals['return'])

if __name__ == "__main__":
    main()


# data = obj.to_buffer().to_pybytes()
# res = requests.post(url="http://localhost:5000",
#                     files={
#                         "data": data,
#                         "meta": pickle.dumps(123)
#                     })
