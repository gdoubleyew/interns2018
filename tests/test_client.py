import pytest
import sys
sys.path.append("..")
import client

client1 = client.Client(args.addr, args.port)

def test_calcDelta():
    assert type(client.calcDelta(client1, "Delta.txt", True)) == type(0.1)

def test_analysis():
    difficulty = 0
    num_results = 0
    client.analysis(client1, "Delta_file", difficulty, num_results)
