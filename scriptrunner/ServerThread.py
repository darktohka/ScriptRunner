import threading
import paramiko

class ServerThread(threading.Thread):

    def __init__(self, server, commands):
        threading.Thread.__init__(self)
        self.daemon = True
        self.server = server
        self.commands = commands
        self.client = None
    
    def run(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Server thread.')