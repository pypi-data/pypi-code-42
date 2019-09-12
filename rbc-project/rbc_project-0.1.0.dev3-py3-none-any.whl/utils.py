import socket
import subprocess
import ipaddress
import netifaces
import uuid
import ctypes


def get_local_ip():
    """Return localhost IP.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return IP


def is_localhost(ip):
    """Check if ip is the IP of a localhost.
    """
    a = ipaddress.ip_address(ip)
    if a.is_loopback:
        return True
    interfaces = netifaces.interfaces()
    mac_list = []
    AF_PACKET = getattr(netifaces, 'AF_PACKET', None)
    if AF_PACKET is None:
        # netifaces version < 0.10.8:
        AF_PACKET = getattr(netifaces, 'AF_LINK', None)
    for i in interfaces:
        ifaddrs = netifaces.ifaddresses(i)
        if netifaces.AF_INET in ifaddrs:
            for ifaddr in ifaddrs[netifaces.AF_INET]:
                if ifaddr.get('addr') == ip:
                    return True
        if AF_PACKET in ifaddrs:
            for ifaddr in ifaddrs[AF_PACKET]:
                mac = ifaddr.get('addr')
                if mac is not None:
                    mac_list.append(mac.replace(':', ''))
    local_mac = hex(uuid.getnode())[2:]
    return local_mac in mac_list


def runcommand(*cmd):
    """Run a command with arguments and return stdout messages.

    The results are cached.
    """
    if cmd not in runcommand.cache:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        runcommand.cache[cmd] = result.stdout.decode()
    return runcommand.cache[cmd]


runcommand.cache = {}


def get_datamodel():
    """Return the data model of a host system.
    """
    short_sizeof = ctypes.sizeof(ctypes.c_short()) * 8
    int_sizeof = ctypes.sizeof(ctypes.c_int()) * 8
    long_sizeof = ctypes.sizeof(ctypes.c_long()) * 8
    ptr_sizeof = ctypes.sizeof(ctypes.c_voidp()) * 8
    longlong_sizeof = ctypes.sizeof(ctypes.c_longlong()) * 8
    return {
        (0,  16,  0, 16,  0): 'IP16',     # PDP-11 Unix
        (16, 16, 32, 16,  0): 'IP16L32',  # PDP-11 Unix
        (16, 16, 32, 32,  0): 'I16LP32',  # MC68000, AppleMac68K, MS x86
        (16, 32, 32, 32,  0): 'ILP32',    # IBM 370, VAX Unix, workstations
        (16, 32, 32, 32, 64): 'ILP32LL',  # MS Win32
        (16, 32, 32, 64, 64): 'LLP64',    # MS Win64
        (16, 32, 64, 64, 64): 'LP64',     # Most UNIX systems
        (16, 64, 64, 64, 64): 'ILP64',    # HAL
        (64, 64, 64, 64, 64): 'SILP64',   # UNICOS
    }[short_sizeof, int_sizeof, long_sizeof, ptr_sizeof, longlong_sizeof]
