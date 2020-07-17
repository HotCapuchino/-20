import numpy as np
import matplotlib.pyplot as plt
import socket
import time
from math import sqrt


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


URL = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((URL, port))
    beat = b"nope"
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)
        im = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])
        #
        max_pos1 = ()
        max_pos2 = ()
        for j in range(200):
            for k in range(200):
                if im[j][k] != 0:
                    if j == 0 and k == 0 and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k + 1] and max_pos1 == ():
                        max_pos1 = (j, k)
                    elif j == 0 and k == 0 and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k + 1]:
                        max_pos2 = (j, k)
                    elif j == 200 and k == 0 and im[j][k] > im[j - 1][k] and im[j][k] > im[j][k + 1] and max_pos1 == ():
                        max_pos1 = (j, k)
                    elif j == 200 and k == 0 and im[j][k] > im[j - 1][k] and im[j][k] > im[j][k + 1]:
                        max_pos2 = (j, k)
                    elif j == 0 and k == 200 and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k - 1] and max_pos1 == ():
                        max_pos1 = (j, k)
                    elif j == 0 and k == 200 and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k - 1]:
                        max_pos2 = (j, k)
                    elif j == 200 and k == 200 and im[j][k] > im[j - 1][k] and im[j][k] > im[j][k - 1] and max_pos1 == ():
                        max_pos1 = (j, k)
                    elif j == 200 and k == 200 and im[j][k] > im[j - 1][k] and im[j][k] > im[j][k - 1]:
                        max_pos2 = (j, k)
                    elif im[j][k] > im[j - 1][k] and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k - 1] \
                            and im[j][k] > im[j][k + 1] and max_pos1 == ():
                        max_pos1 = (j, k)
                    elif im[j][k] > im[j - 1][k] and im[j][k] > im[j + 1][k] and im[j][k] > im[j][k - 1] \
                            and im[j][k] > im[j][k + 1]:
                        max_pos2 = (j, k)
        if max_pos2 == ():
            result = 0.0
        else:
            delta = np.abs(np.array(max_pos1) - np.array(max_pos2))
            result = round(sqrt(delta[0] ** 2 + delta[1] ** 2), 1)
        sock.send(f"{result}".encode())
        resp = sock.recv(20)
        sock.send(b"beat")
        beat = sock.recv(20)
        plt.imshow(im)
        plt.pause(0.5)
        plt.show()
print("Done")