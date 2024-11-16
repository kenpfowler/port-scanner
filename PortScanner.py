import socket
import logging


# What is a port scanner?
# a port scanner is a program that attempts to enumerate which ports are open on a machine.
# network capable processes need to listen on a port in order to accept incoming messages
# a port scanner would likely take advantage of this necessary behavior in order to test if a port is open on a device
# there are two types of Transport Layer protocols that can receive messages over a network: TCP and UDP
# tcp is connection oriented so we might be able to simple connect to a tcp port and then close the connection if we get an ACK response
# upd is maybe a little tricky... we can send data to a udp port without a connection. delivery is best effort and there is no obligation for the client to respond...
# therefore ill need to do research for testing a udp port for openness, maybe my assumption is wrong and clients are obliged to respond (there is a checksum after all)
# a port is identified with a 16 bit number so that 2^16 or 65536 ports
# apparently we dont use port 0 because it is reserved so that leaves 65535 ports that can be open or closed

# ports 0 to 1023 are Well-Known Ports. 
# These ports are assigned to a specific server sevice, eg, port 80 is used by web servers. 
# Ports 1024 to 49151 are Registered Ports. These ports can be registered by developers to designate a particular port for their application. 
# Ports 49152 to 65535 are Public Ports.

class PortScanner:
    def __init__(self, host = "localhost", port = 80):
         self.host = host
         self.port = port
         self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
         self.logger = logging.getLogger(__name__)
         self.max_port = 65535

    def handle_tcp_connection(self):
        try:
            self.tcp_sock.connect((self.host, self.port))
            self.logger.info("socket is open to tcp connection")
        except KeyboardInterrupt:
            self.logger.info("aborting scan")
        except ConnectionRefusedError:
            self.logger.info("socket is not open to tcp connection")
        except Exception as e:
            self.logger.error(f"error was raised: {e}")
        
    def start(self):
        self.logger.info(f"scanning port {self.port} on host {self.host}")
        self.handle_tcp_connection()
        self.tcp_sock.close()
