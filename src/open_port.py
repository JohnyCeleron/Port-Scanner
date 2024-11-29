from dataclasses import dataclass
from typing import Optional
from src.protocol_enum import TransportProtocol


@dataclass
class OpenPort:
    transport_protocol: TransportProtocol
    port_number: int
    time: Optional[float] = None
    application_protocol: str = '-'
    guess: bool = False
    verbose: bool = False

    def __str__(self) -> str:
        time = self.time if self.verbose and self.transport_protocol == TransportProtocol.TCP else ""
        app_protocol = self.application_protocol if self.guess else ""
        return f'{self.transport_protocol.value} {self.port_number} {time} {app_protocol}'