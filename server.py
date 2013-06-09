import SocketServer
from mixins import ThreadPoolMixIn, OtherPoolMixIn
import re
import threading
import os


class MyRequestHandler(SocketServer.BaseRequestHandler):
    users = {}

    def handle(self):
        # print threading.currentThread().getName()
        # print "Pid: %d" % os.getpid()

        command = self.request.recv(1024).strip()
        print command
        #import pdb;pdb.set_trace()
        match = re.search('user (?P<user>\w+)', command)
        if match:
            user = match.group('user')
            if user and user in self.users:
                response = "100 err %s already taken!\r\n" % user
            else:
                self.users[user] = self.request
                response = "200 ok %s successfully registerred" % user
            #import pdb;pdb.set_trace()
            self.request.send(response)
            return
        match  = re.search('send_to (?P<user>\w+) (?P<message>.*)', command)
        if match:
            user, message = match.groups()
            if user in self.users:
                self.users[user].send(message)
                self.request.send("200 ok message to %s sent successfully.\r\n" % user)
            else:
                self.request.send("100 err %s does not exists!\r\n" % user)
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
