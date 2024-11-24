import argparse
import asyncio

from PortScanner import PortScanner


def validate_ip_range(ip_range):
    """Validate and parse an IP address range in the format 'start_ip-end_ip'."""
    try:
        start_ip, end_ip = ip_range.split("-")
        # Optionally, you could validate the IP addresses using socket or a regex
        return start_ip, end_ip
    except ValueError:
        raise argparse.ArgumentTypeError(
            "IP range must be in the format 'start_ip-end_ip'."
        )


async def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Scan for open ports on a device.")

    # TODO: support an ip range feature
    # Add argument for IP range
    # parser.add_argument(
    #     "ip_range",
    #     type=validate_ip_range,
    #     help="Specify the range of IP addresses in the format 'start_ip-end_ip'."
    # )

    # Add optional argument for specific ports or port ranges
    parser.add_argument(
        "-p",
        "--ports",
        type=str,
        default="1-65535",  # Default to all ports
        help="Specify port(s) to scan, e.g., '80', '20-25', or '80,443,8080'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Extract the parsed arguments
    # TODO: support an ip range feature
    # start_ip, end_ip = args.ip_range
    ports = args.ports

    # Add logic for scanning IPs and ports here...
    scanner = PortScanner(host="localhost", ports=ports)
    await scanner.start()

if __name__ == "__main__":
    asyncio.run(main())
