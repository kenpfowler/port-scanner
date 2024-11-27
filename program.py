import argparse
import asyncio

from PortScanner import PortScanner


async def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Scan for open ports on a device.")

    # TODO: support an ip range feature
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Specify the range of hostname of the device you want to scan e.g., localhost, scanme.nmap.org",
    )

    # Add optional argument for specific ports or port ranges
    parser.add_argument(
        "--ports",
        type=str,
        default="1-65535",  # Default to all ports
        help="Specify port(s) to scan, e.g., '80', '20-25', or '80,443,8080'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    host = args.host
    ports = args.ports

    # Add logic for scanning IPs and ports here...
    scanner = PortScanner(host=host, ports=ports)
    await scanner.start()


if __name__ == "__main__":
    asyncio.run(main())
