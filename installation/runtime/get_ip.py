import socket

# Copied from: https://www.w3resource.com/python-exercises/python-basic-exercise-55.php
def get_ip():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                         if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                               s.getsockname()[0], s.close()) for s in
                                                              [socket.socket(socket.AF_INET,
                                                                             socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
