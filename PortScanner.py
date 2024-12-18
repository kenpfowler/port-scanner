import socket
import logging
import time
import asyncio

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

# Nmap scan report for localhost (127.0.0.1)
# Host is up (0.00010s latency).
# Not shown: 995 closed tcp ports (conn-refused)
# PORT      STATE SERVICE
# 80/tcp    open  http
# 443/tcp   open  https
# 631/tcp   open  ipp
# 5432/tcp  open  postgresql
# 10000/tcp open  snet-sensor-mgmt


class PortScanner:
    max_port = 65535
    min_port = 1

    def __init__(self, host="localhost", ports="1-65535", concurrency_limit=1000):
        self.concurrency_limit = concurrency_limit
        self.host = host
        self.ip = socket.gethostbyname(host)
        self.ports = ports
        self.port_range = self.parse_port_range(ports)
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        self.results = []

    def parse_port_range(self, port_range):
        try:
            # Split the input string
            start, end = map(int, port_range.split("-"))

            # Ensure the range is valid
            if start > end or start < self.min_port or end > self.max_port:
                raise ValueError(
                    "Invalid port range. Must be between 1 and 65535, and start <= end."
                )

            # Generate the list of ports
            return list(range(start, end + 1))

        except ValueError as e:
            raise ValueError(f"Invalid port range format: {e}")

    async def check_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)

        try:
            await asyncio.wait_for(
                asyncio.get_event_loop().sock_connect(sock, (self.ip, port)), 1
            )
            self.results.append((port, "OPEN"))
        except ConnectionRefusedError:
            self.results.append((port, "CLOSED"))
        except asyncio.TimeoutError:
            self.results.append((port, "FILTERED"))
        except KeyboardInterrupt:
            self.logger.info("aborting scan")
        except Exception as e:
            self.logger.error(f"error was raised: {e}")
        finally:
            sock.close()

    def chunk_ports(self):
        total_ports = len(self.port_range)

        for i in range(0, total_ports, self.concurrency_limit):
            ports = self.port_range[i : i + self.concurrency_limit]
            tasks = [asyncio.create_task(self.check_port(port)) for port in ports]
            yield tasks

    async def start(self):
        self.logger.info(f"scanning ports {self.ports} on host {self.ip}")
        start_time = time.perf_counter()

        for tasks in self.chunk_ports():
            await asyncio.gather(*tasks)

        end_time = time.perf_counter()
        duration = end_time - start_time

        self.logger.info(f"scan completed in {duration:.2f} seconds")
        filtered = [result for result in self.results if result[1] == "OPEN"]
        for connection in filtered:
            self.logger.info(f"port - {connection[0]} status - {connection[1]}")
