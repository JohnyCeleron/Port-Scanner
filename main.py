from port_scaner_request import PortScanRequest
from port_scaner_response import PortScanResponse
from console_parser import get_arguments

def main():
    arguments = get_arguments()
    request = PortScanRequest.from_argument_parser(arguments)
    response = PortScanResponse(request)
    print(response)

if __name__ == '__main__':
    main()