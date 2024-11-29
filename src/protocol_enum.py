from enum import StrEnum


class TransportProtocol(StrEnum):
    TCP = 'TCP',
    UDP = 'UDP'


class ApplicationProtocol(StrEnum):
    HTTP = 'HTTP',
    DNS = 'DNS',
    ECHO = 'ECHO',