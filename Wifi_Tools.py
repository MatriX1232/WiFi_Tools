import socket
from threading import Thread, Lock
# from subprocess import Popen, PIPE
import subprocess


def IP_Scanner(msg: str, PORTS: list) -> dict:
    lock = Lock()
    IPs = {}

    class Thread_IP_Scanner(Thread):
        def __init__(self, IP, PORTS, MSG):
            Thread.__init__(self)
            self.IP = IP
            self.PORTS = PORTS
            self.msg = MSG
            self.port = None
            self.daemon = True
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def checkIfValid(self):
            length = int(self.s.recv(1024).decode('utf-8'))
            response = self.s.recv(length).decode('utf-8')
            if response == "<LIVE-SERVER-MS>":
                lock.acquire()
                IPs[self.IP] = self.port
                # print("Found port on  << ", self.IP, self.port)
                lock.release()
            self.s.close()

        def run(self):
            self.s.settimeout(1)
            for port in self.PORTS:
                self.port = port
                if self.s.connect_ex((self.IP, self.port)) == 0:
                    self.checkIfValid()
            return

    THREADS = []
    for IP in range(1, 256):
        ip = "192.168.0." + str(IP)
        th = Thread_IP_Scanner(ip, PORTS.copy(), msg)
        th.start()
        THREADS.append(th)

    # print(len(THREADS), THREADS)
    for i in range(1, 256):
        try:    THREADS[i].join()
        except: pass
        # THREADS.pop(i)
    # print("THREADS: ", THREADS)
    return IPs


class NetworkStats:
    def getLanIP():
        proc = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE)
        result = proc.stdout.readlines()
        scan = 0
        flag = False
        for l in result:
            if b"Wireless LAN adapter Wi-Fi:\r\n" == l:
                flag = True
            if flag:
                scan += 1
            if scan == 5:
                return l.decode().strip().split(":")[1][1:]
        raise Exception("Cannot find LAN IP")

    def getFreePorts():
        proc = subprocess.Popen(['netstat', '-ano'], stdout=subprocess.PIPE)
        result = proc.stdout.readlines()
        flag = False
        ports = []  # Proto, Local Address, Foreign Address, State, PID
        for l in result:
            if b'  Proto  Local Address          Foreign Address        State           PID\r\n' == l:
                flag = True
            if flag:
                ports.append(l.decode().split())

        freePorts = []
        for port in ports:
            if "LISTENING" in port and int(port[4]) > 6000:
                freePorts.append(port[4])

        return freePorts


# if __name__ == "__main__":
#     PORTS = [9999, 10000, 10001]
    # THREADS = []
    # for IP in range(1, 257):
    #     ip = "192.168.0." + str(IP)
    #     th = Thread_IP_Scanner(ip, PORTS.copy()).start()
        # THREADS.append(th)

    # for i in range(1, 257):
    #     try:
    #         THREADS[i].join(0.1)
    #         THREADS.pop(i)
    #     except: pass

    # print(IPs)