import getopt, sys
from PortScanner import PortScanner

# Remove 1st argument from the
# list of command line arguments
argument_list = sys.argv[1:]

# Options
options = "hp:"

# Long options
long_options = ["host=", "port="]

host = "localhost"
port = 8080

try:
    # Parsing argument
    arguments, values = getopt.getopt(argument_list, options, long_options)
    
    # checking each argument
    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--host"):
            host = current_value
            print (("specified host (% s)") % (current_value))
            
        elif current_argument in ("-p", "--port"):
            port = int(current_value)
            print (("specified port (% s)") % (current_value))
            
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


port_scanner = PortScanner(host, port, servers)

port_scanner.start()


