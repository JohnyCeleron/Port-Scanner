import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Port scanner utility",
        usage="portscan [OPTIONS] IP_ADDRESS [{tcp|udp}[/[PORT|PORT-PORT],...]]..."
    )
    _add_optional_arguments(parser)
    _add_positional_arguments(parser)
    return parser.parse_args()


def _add_positional_arguments(parser):
    parser.add_argument("ip_address", type=str,
                        help="IP address to scan"
                        )
    parser.add_argument("ports", nargs="*",
                        help="Protocols and ports to scan, e.g., tcp/80, udp/53-100"
                        )


def _add_optional_arguments(parser):
    parser.add_argument("--timeout", type=float, default=2.0,
                        help="Timeout for waiting response in seconds (default: 2s)"
                        )
    parser.add_argument("-j", "--num-threads", type=int, default=1,
                        help="Number of threads for scanning (default: 1)"
                        )
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose mode"
                        )
    parser.add_argument("-g", "--guess", action="store_true",
                        help="Try to guess the application layer protocol"
                        )
