from argparse import Namespace
from dataclasses import dataclass
from src.protocol_enum import TransportProtocol


@dataclass
class Options:
    numberThreads: int
    verbose: bool
    guess: bool
    timeout: float

@dataclass
class Port:
    protocol: TransportProtocol
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
            if '/' not in port:
                protocol = TransportProtocol.TCP if port == "tcp" else TransportProtocol.UDP
                for i in range(1, 65536):
                    list_ports.append(Port(protocol, i))
                continue

            data = port.split('/')
            protocol = TransportProtocol.TCP if data[0] == 'tcp' else TransportProtocol.UDP
            for t in data[1].split(','):
                if '-' not in t:
                    list_ports.append(Port(protocol, int(t)))
                    continue
                start, end = map(int, t.split('-'))
                for i in range(start, end + 1):
                    list_ports.append(Port(protocol, int(i)))
        return cls(options, ip_address, list_ports)