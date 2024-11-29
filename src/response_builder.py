from dataclasses import dataclass
from src.request_builder import PortScanRequest, Port, Options
from src.protocol_enum import TransportProtocol
from src.scanner import scan_udp, scan_tcp
from src.open_port import OpenPort
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class PortScanResponse:
    open_ports: list[OpenPort]

    @classmethod
    def from_request(cls, request: PortScanRequest):
        open_ports = cls._found_open_ports(request.list_ports, request.options, request.ip_address)
        return cls(open_ports)

    @staticmethod
    def _found_open_ports(list_ports: list[Port], options: Options, ip_address: str) -> list[OpenPort]:
        open_ports = []
        num_threads = options.numberThreads

        def scan_port(port: Port) -> OpenPort | None:
            if port.protocol == TransportProtocol.UDP:
                return scan_udp(ip_address, port.number, options)
            else:
                return scan_tcp(ip_address, port.number, options)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(scan_port, port): port for port in list_ports}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        return open_ports

    def __str__(self) -> str:
        return '\n'.join(str(port) for port in self.open_ports)