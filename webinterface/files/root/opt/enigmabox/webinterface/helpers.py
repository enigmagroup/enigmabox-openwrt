
def normalize_ipv6(ipv6):
    return ':'.join([str(x).zfill(4) for x in ipv6.split(':')])

