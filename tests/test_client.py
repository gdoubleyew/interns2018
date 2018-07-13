import pytest
import sys
import os
sys.path.append("..")
import client


@pytest.fixture(scope="module")
def getClient():  # type: ignore
    cl = client.Client("localhost", 5200)
    return cl


# makes random clockSkew offset
clockSkew_offset = 0
clockSkew_file = "ClockSkew_test.txt"


def remove_file(clockSkew_file):
    if os.path.exists(clockSkew_file):
        os.remove(clockSkew_file)


def test_calcClockSkew_posative():
    clockSkew_offset = 10
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient(), clockSkew_file, True, clockSkew_offset)
    assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_calcClockSkew_negative():
    clockSkew_offset = -10
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient(), clockSkew_file, True, clockSkew_offset)
    assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_analysis_completes():
    difficulty = [1, -1]
    for diff in difficulty:
        remove_file(clockSkew_file)
        succsesful, time_took, deadlineTime = client.analysis(getClient(), clockSkew_file, diff)
        print(succsesful, time_took, deadlineTime)
        assert succsesful == "succses"
        assert round(time_took, 1) <= round(deadlineTime, 1)


def test_analysis_fails():
    difficulty = [3, -3]
    for diff in difficulty:
        remove_file(clockSkew_file)
        succsesful, time_took, deadlineTime = client.analysis(getClient(), clockSkew_file, diff)
        assert succsesful == "failed"
        assert round(time_took, 1) == round(deadlineTime, 1)


# the None checks for code
def test_analysis_none():
    remove_file(clockSkew_file)
    succsesful, time_took, deadlineTime = client.analysis(getClient(), None, None)
    assert round(time_took, 1) <= round(deadlineTime, 1)


def test_analysis_noArgs():
    remove_file(clockSkew_file)
    succsesful, time_took, deadlineTime = client.analysis(getClient())
    assert round(time_took, 1) <= round(deadlineTime, 1)


def test_calcClockSkew_none():
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient(), None, None, None)
    assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_calcClockSkew_noArgs():
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient())
    assert round(retVal, 2) == round(clockSkew_offset, 2)

def test_calcClockSkew_numreplace():
    clockSkew_offset = 3
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient(),1,2,3)
    assert round(retVal, 2) == round(clockSkew_offset, 2)

def test_calcClockSkew_numreplace():
    clockSkew_offset = 3
    remove_file(clockSkew_file)
    retVal = client.calcClockSkew(getClient(),"6,7,9","3,2,4,5,5",clockSkew_offset)
    # variation of test_offset fails..
    assert round(retVal, 2) == round(clockSkew_offset, 2)
