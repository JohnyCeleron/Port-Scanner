from typing import Optional

from scapy.all import (
    DNS, DNSQR, IP, sr1, UDP, TCP, ICMP
)

from src.protocol_enum import ApplicationProtocol, TransportProtocol

TIME_OUT = 5

STANDART_PROTOCOLS = {
    80: ApplicationProtocol.HTTP,
    53: ApplicationProtocol.DNS,
    7: ApplicationProtocol.ECHO
}

def _is_http_protocol(ip_target: str, port: int, transport_protocol: TransportProtocol) -> bool:
    if transport_protocol == TransportProtocol.TCP:
        try:
            http_request = f"GET / HTTP/1.1\r\nHost: {ip_target}\r\n\r\n"
            _tcp_connect(ip_target, port)
            http_response = sr1(IP(dst=ip_target) / TCP(dport=port, flags="PA") / http_request, verbose=0,
                                timeout=TIME_OUT)
            return http_response is not None and b"HTTP" in bytes(http_response)
        except ConnectionError:
            return False
    return False


def _is_echo_protocol(ip_target: str, port: int, transport_protocol: TransportProtocol) -> bool:
    echo_request = IP(dst=ip_target) / ICMP()
    response = sr1(echo_request, verbose=0, timeout=TIME_OUT)
    return response is not None and response.haslayer(ICMP) and response.getlayer(ICMP).type == 0

def _is_dns_protocol(ip_target: str, port: int, transport_protocol: TransportProtocol) -> bool:
    dns_packet = DNS(rd=1, qd=DNSQR(qname="www.google.com"))
    response = None
    if transport_protocol == TransportProtocol.UDP:
        response = sr1(IP(dst=ip_target)/UDP(dport=port)/dns_packet,
                       verbose=0, timeout=TIME_OUT)
    try:
        _tcp_connect(ip_target, port)
        response = sr1(IP(dst=ip_target)/TCP(dport=port)/dns_packet, verbose=0, timeout=TIME_OUT)
    except ConnectionError:
        return False
    if response and response.haslayer(DNS):
        dns_layer = response.getlayer(DNS)
        return dns_layer.rcode == 0 and dns_layer.qr == 1
    return False


def _tcp_connect(ip_target: str, port: int):
    packet = IP(dst=ip_target) / TCP(dport=port, flags="S")
    response = sr1(packet, verbose=0)
    if response:
        if response.getlayer(TCP).flags == "SA":
            sr1(IP(dst=ip_target) / TCP(dport=port, flags="A"), verbose=0, timeout=TIME_OUT)
            return
    raise ConnectionError("Не удалось установить TCP соединение")


def guess_protocol(ip_target: str, port: int, transport_protocol: TransportProtocol) -> Optional[ApplicationProtocol]:
    if port in STANDART_PROTOCOLS:
        if port != 80 or (port == 80 and transport_protocol.UDP):
            return STANDART_PROTOCOLS[port]

    if _is_http_protocol(ip_target, port, transport_protocol):
        return ApplicationProtocol.HTTP
    if _is_dns_protocol(ip_target, port, transport_protocol):
        return ApplicationProtocol.DNS
    if _is_echo_protocol(ip_target, port, transport_protocol):
        return ApplicationProtocol.ECHO