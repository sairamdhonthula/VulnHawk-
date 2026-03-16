import socket

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, int(port)))
        banner = s.recv(1024)
        s.close()
        return banner.decode(errors="ignore").strip()
    except Exception:
        return None
