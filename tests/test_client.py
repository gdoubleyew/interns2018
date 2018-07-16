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


def test_calcClockSkew_positive():
    clockSkew_offset = 10
    remove_file(clockSkew_file)
    retVal, ignor = client.calcClockSkew(getClient(), clockSkew_file, True, clockSkew_offset)
    assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_calcClockSkew_negative():
    clockSkew_offset = -10
    remove_file(clockSkew_file)
    retVal, ignor = client.calcClockSkew(getClient(), clockSkew_file, True, clockSkew_offset)
    assert round(retVal, 2) == round(clockSkew_offset, 2)

# def test_calcClockSkew_none():
#     remove_file(clockSkew_file)
#     retVal, ignor = client.calcClockSkew(getClient(), None, None, None)
#     assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_calcClockSkew_noArgs():
    remove_file(clockSkew_file)
    retVal, ignor = client.calcClockSkew(getClient())
    assert round(retVal, 2) == round(clockSkew_offset, 2)


def test_calcClockSkew_NoClient():
    remove_file(clockSkew_file)
    try:
        client.calcClockSkew(None)
    except ValueError:
        assert True


def test_calcClockSkew_resetFalse():
    clockSkew_offset = 0
    TorF = [True, False]
    vals = []
    remove_file(clockSkew_file)
    for boolean in TorF:
        retVal, ignor = client.calcClockSkew(getClient(), clockSkew_file, boolean, clockSkew_offset)
        vals.append(retVal)
    assert vals[0] == vals[1]


def test_calcClockSkew_resetTrue():
    clockSkew_offset = 0
    vals = []
    remove_file(clockSkew_file)
    for boolean in range(0, 2):
        retVal, ignor = client.calcClockSkew(getClient(), clockSkew_file, True, clockSkew_offset)
        vals.append(retVal)
    assert not (vals[0] == vals[1])


# analysis Tests
def test_analysis_completes():
    difficulty = 1
    remove_file(clockSkew_file)
    succsesful, time_took, deadlineTime = client.analysis(getClient(), clockSkew_file, difficulty)
    print(succsesful, time_took, deadlineTime)
    assert succsesful == "succses"
    assert round(time_took, 1) <= round(deadlineTime, 1)


def test_analysis_fails():
    difficulty = 3
    remove_file(clockSkew_file)
    succsesful, time_took, deadlineTime = client.analysis(getClient(), clockSkew_file, difficulty)
    print("deadline: {}, took: {}".format(deadlineTime, time_took))
    assert succsesful == "failed"
    assert round(time_took, 1) == round(deadlineTime, 1)

    # the None checks for code
    # def test_analysis_none():
    #     remove_file(clockSkew_file)
    #     succsesful, time_took, deadlineTime = client.analysis(getClient(), None, None)
    #     assert round(time_took, 1) <= round(deadlineTime, 1)

    # def test_analysis_noArgs():
    #     remove_file(clockSkew_file)
    #     succsesful, time_took, deadlineTime = client.analysis(getClient())
    #     assert round(time_took, 1) <= round(deadlineTime, 1)
