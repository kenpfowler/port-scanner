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
class PortScanner:
    def __init__(self, host = "localhost", port = 8080):
         self.host = host
         self.port = port
         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
         self.logger = logging.getLogger(__name__)


    def start(self):
        self.logger.info(f"scanning port {self.port} on host {self.host}")