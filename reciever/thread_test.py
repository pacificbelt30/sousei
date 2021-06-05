import threading
import time

def a():
    for i in range(1000000):
        print("a",i)

def b():
    n = 100
    for i in range(int(n)):
        print("b",i)

thread1 = threading.Thread(target=a)
thread2 = threading.Thread(target=b)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
