import socket
import datetime
import os
import timeit
import threading
import time
import sys
from Queue import Queue

HOST = 'localhost'
PORT = 53617
BUFSIZE = 1024
ADDR = (HOST, PORT)

def make_requests(times=1):
    for i in xrange(times):
        message = raw_input("> ")
        if not message:
            break
        # message = "user blabla%d" % i
        try:
            messages.put(message)

            # Receive data from the server and shut down
            #received = s.recv(1024)
            # end_time = datetime.datetime.now()
            #print "Received : %s" % received
            # microseconds = (end_time - start_time).microseconds
            # print "Thread: %s ; RequestNo: %d ;Time %s" % (threading.currentThread().getName(), i, repr(microseconds))
        except:
            pass
        # finally:
        #     s.close()

def receive_msg():
    while True:
        time.sleep(3)
        try:
            tcpCliSock.sendall(messages.get())
            received = tcpCliSock.recv(BUFSIZE)
            if received:
                print "Message received: %s" % repr(received)
        except:
            pass

def test():
    start_time = datetime.datetime.now()
    for client in xrange(1, 500):
        t = threading.Thread(target=make_requests, args=(100, ))
        # t.setDaemon(True) # don't hang on exit
        t.setName("Thread%d" % client)
        t.start()
        t.join()
    end_time = datetime.datetime.now()
    print "Total time: %d" % (end_time-start_time).seconds

if __name__ == '__main__':
    # test()
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)

    messages = Queue()

    t = threading.Thread(target=receive_msg)
    t.setDaemon(True) # don't hang on exit
    t.start()

    while True:
        make_requests()
    # pid = os.fork()
    # if pid:
    #     continue
    # else:
    #     print "PID %d: %f" % (os.getpid(), timeit.timeit('make_requests(30)', setup='from __main__ import make_requests', number=1))
    #     os._exit(0)

