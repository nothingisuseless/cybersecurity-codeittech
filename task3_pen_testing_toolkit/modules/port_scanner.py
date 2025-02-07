import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open on {target}")
        sock.close()
    except Exception as e:
        pass

def scan_target(target, ports):
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda port: scan_port(target, port), ports)

if __name__ == '__main__':
    target_ip = input("Enter target IP address: ")
    ports = range(1, 65535)
    scan_target(target_ip, ports)
