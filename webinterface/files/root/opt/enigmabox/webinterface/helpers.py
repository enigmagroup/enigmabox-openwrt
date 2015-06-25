
def normalize_ipv6(ipv6):
    return ':'.join([str(x).lstrip('0') for x in ipv6.split(':')])

