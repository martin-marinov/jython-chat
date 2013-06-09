import SocketServer
from mixins import ThreadPoolMixIn, OtherPoolMixIn
import re
import threading
import os


class MyRequestHandler(SocketServer.StreamRequestHandler):
    users = {}

    def handle(self):
        # print threading.currentThread().getName()
        # print "Pid: %d" % os.getpid()
        command = self.rfile.readline().strip()
        user = re.search('user (\w+)', command)
        response = None
        if user:
            user = user.group(1)
            if user and user in self.users:
                response = "100 err %s already taken!" % user
            else:
                self.users[user] = self.client_address
                response = "200 ok %s successfully registerred" % user
        #import pdb;pdb.set_trace()
        self.wfile.write(response)
        return


class MyThreadedServer(ThreadPoolMixIn, SocketServer.TCPServer):
    numThreads = 300

class MyForkedServer(SocketServer.ForkingTCPServer):
    max_children = 40

class MyOtherServer(OtherPoolMixIn, SocketServer.TCPServer):
    numThreads = 2


# class COMMANDS:



# class CommandParser:
#     def __init__(self, request):
#         command = request.recv(1024).decode('utf8')

if __name__ == '__main__':
    address = ('localhost', 53617)  # let the kernel give us a port
    server = MyOtherServer(address, MyRequestHandler)

    server.serve_forever()
