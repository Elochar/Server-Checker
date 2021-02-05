"""
Cole Hartnett 1/13/2021
This is a server mointor for a personal network
The code was gotten from Clarity coders
This code allows to mointor devices on a network,
check for open ports, apply ssl if needed, and also ping computers.
"""

import socket
import ssl
from datetime import datetime
import pickle

import subprocess
import platform

from gmail import email_alert


class Server():
    #define the server and inputs
    def __init__(self, name, port, connection, priority):
        #define the Server attributes
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()

        #create a list to store the history of the server
        self.history = []
        #check flag for sending the alert.
        self.alert = False

    def check_connection(self):
        msg = ""
        # by default assume the connection success is false.
        success = False
        now = datetime.now()

        #use try except to handle the different types of connection
        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                #assuming there is a ssl connection, wrap the socket in ssl
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            else:
                #if there is no ssl then treat the connection like a ping.
                if self.ping():
                    msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"server: {self.name} timeout. On port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"No Clue??: {e}"

        if success == False and self.alert == False:
            # Send Alert
            self.alert = True
            email_alert(self.name,f"{msg}\n{now}","chpopo12@gmail.com")

        self.create_history(msg, success, now)
    #history create function
    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg, success, now))

        while len(self.history) > history_max:
            self.history.pop(0)
    #ping function
    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
            return False


if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        servers = [
            Server("reddit.com", 80, "plain", "high"),
            Server("krebsonsecurity.com", 80, "plain", "high"),
            Server("evo.com", 465, "ssl", "high"),
            Server("2601:19b:c502:b0d0::8e8c", 80, "ping", "high"),
            Server("google", 80, "plain", "high")
        ]

    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    pickle.dump(servers, open("servers.pickle", "wb"))
