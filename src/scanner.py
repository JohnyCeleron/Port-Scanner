from src.protocol_enum import TransportProtocol
from src.request_builder import Options
from src.open_port import OpenPort
import time
from typing import Optional
from scapy.all import send, TCP, IP, sr1, Raw, UDP, ICMP
from src.protocol_guesser import guess_protocol


def scan_tcp(ip_target: str, port: int, options: Options) -> Optional[OpenPort]:
    syn_packet = IP(dst=ip_target) / TCP(dport=port, flags="S")
    start = time.time()
    response = sr1(syn_packet, timeout=options.timeout, verbose=0)
    if response and response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)
        if tcp_layer.flags == "SA":
            protocol = guess_protocol(ip_target, port, TransportProtocol.TCP) if options.guess else "-"
            end = time.time()
            time_in_ms = (end - start) * 1000
            return OpenPort(port_number=port,transport_protocol=TransportProtocol.TCP,
                            time=time_in_ms, guess=options.guess, verbose=options.verbose,
                            application_protocol=protocol)


def scan_udp(ip_target: str, port: int, options: Options) -> Optional[OpenPort]:
    udp_packet = sr1(IP(dst=ip_target)/UDP(dport=port), timeout=options.timeout, verbose=0)
    if udp_packet is None or (udp_packet.haslayer(UDP) and not udp_packet.haslayer(ICMP)):
        protocol = guess_protocol(ip_target, port, TransportProtocol.UDP) if options.guess else "-"
        return OpenPort(port_number=port, transport_protocol=TransportProtocol.UDP,
                        guess=options.guess, verbose=options.verbose, application_protocol=protocol)