from argparse import Namespace
from dataclasses import dataclass
from enum import Enum

@dataclass
class Options:
    numberThreads: int
    verbose: bool
    guess: bool
    timeout: int

class Protocol(Enum):
    TCP = 'TCP',
    UDP = 'UDP'

@dataclass
class Port:
    protocol: Protocol
    number: int

@dataclass
class PortScanRequest:
    options: Options
    ip_address: str
    list_ports: list[Port]

    @classmethod
    def from_argument_parser(cls, args: Namespace):
        options = Options(args.num_threads, args.verbose, args.guess, args.timeout)
        ip_address = args.ip_address
        list_ports = []
        for port in args.ports:
            data = port.split('/')
            protocol = Protocol.TCP if data[0] == 'tcp' else Protocol.UDP
            for t in data[1].split(','):
                if '-' not in t:
                    list_ports.append(Port(protocol, int(t)))
                    continue
                start, end = map(int, t.split('-'))
                for i in range(start, end + 1):
                    list_ports.append(Port(protocol, int(i)))
        return cls(options, ip_address, list_ports)