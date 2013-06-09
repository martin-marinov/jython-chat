import socket
import datetime
import os
import timeit
import threading
import time

# errors = 0

def make_requests(times):
    for i in xrange(times):
        # message = raw_input("> ")
        message = "user blabla%d" % i
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            HOST, PORT = ('127.0.0.1', 53617)
            # Connect to server and send data
            # start_time = datetime.datetime.now()
            s.connect((HOST, PORT))
            s.sendall(message + "\n")

            # Receive data from the server and shut down
            received = s.recv(1024)
            # end_time = datetime.datetime.now()
            # print "Received : %s" % received
            # microseconds = (end_time - start_time).microseconds
            # print "Thread: %s ; RequestNo: %d ;Time %s" % (threading.currentThread().getName(), i, repr(microseconds))
        # except:
        #     global errors
        #     errors += 1
        finally:
            s.close()

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    for client in xrange(1, 500):
        t = threading.Thread(target=make_requests, args=(100, ))
        # t.setDaemon(True) # don't hang on exit
        t.setName("Thread%d" % client)
        t.start()
        t.join()
    end_time = datetime.datetime.now()
    print "Total time: %d" % (end_time-start_time).seconds
        # pid = os.fork()
        # if pid:
        #     continue
        # else:
        #     print "PID %d: %f" % (os.getpid(), timeit.timeit('make_requests(30)', setup='from __main__ import make_requests', number=1))
        #     os._exit(0)

