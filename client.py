import requests
import pickle
import argparse
import time
# import subprocess

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

    def put(self, request_id, value):
        data = pickle.dumps(value)
        res = requests.post(url=self.url,
                            files={
                                "value": data,
                                "request_id": request_id
                            })
        return res

    def get(self, params):
        res = requests.get(url=self.url, params=params)
        # objects = self.serialization_context.deserialize(res.raw.read())
        return res


def main():
    parser = argparse.ArgumentParser(description="Realtime Client")
    parser.add_argument('-a', action="store", dest="addr", default="localhost")
    parser.add_argument('-p', action="store", dest="port", default=5200)
    #parser.add_argument('-r', action="store", default = False)
    args = parser.parse_args()
    client = Client(args.addr, args.port)

    rtt_list = []
    total = []

    for i in range(0,100):
        client_ts = time.time()
        params = {
        "request_id": 1,
        "client_ts": client_ts
        }
        res = client.get(params)
        client_ts2 = time.time()
        vals = res.json()
        server_ts = vals['server_ts']

        rtt = client_ts2 - client_ts
        rtt_list.append(rtt)

        TT = rtt/2
        D = client_ts2 - server_ts - TT
        total.append(D)

    min_T = min(rtt_list)
    best_val = total[rtt_list.index(min_T)]
    print("Total: {}".format(best_val))

if __name__ == "__main__":
    main()


# data = obj.to_buffer().to_pybytes()
# res = requests.post(url="http://localhost:5000",
#                     files={
#                         "data": data,
#                         "meta": pickle.dumps(123)
#                     })
