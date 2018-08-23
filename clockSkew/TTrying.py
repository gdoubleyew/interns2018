import threading
import time
import random

def alarm1(sec):
    ms = sec * 1000
    print("In thread alarm")
    for i in range(0, ms):
        time.sleep(0.001)
    return "BEEP!!!"

def work():
    print("In thread work")
    num = random.randint(1,3)
    time.sleep(num)
    return "OK"

workT = threading.Thread(target=work)
alarmT = threading.Thread(target=alarm1, args=(2,))
B = alarmT.start()
As = workT.start()

workT.join()
alarmT.join()

print(As)
#
#
# import threading
#
#
# def worker():
#     """thread worker function"""
#     print('Worker')
#
#
# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start()
