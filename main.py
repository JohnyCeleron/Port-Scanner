from src.request_builder import PortScanRequest
from src.response_builder import PortScanResponse
from console_parser import get_arguments


def main():
    arguments = get_arguments()
    print(arguments)
    request = PortScanRequest.from_argument_parser(arguments)
    response = PortScanResponse.from_request(request)
    print(response)

if __name__ == '__main__':
    main()