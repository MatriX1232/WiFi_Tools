import socket
import threading
import time


class NetworkBeacon:
    def __init__(self, PORT, BEACON_MSG):
        self.PORT = PORT
        self.MSG = BEACON_MSG
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.THREADS = []
        self.CONNS = []

    def thread_handle(self, conn):
        print(f"Client connected: {conn}")
        msg = self.MSG.encode('utf-8')
        length = str(len(msg)).zfill(1024)
        conn.send(length.encode('utf-8'))
        conn.send(msg)
        time.sleep(1)
        conn.close()
        return

    def stop(self):
        self.s.close()
        for conn in self.CONNS:
            conn.close()

        for th in self.THREADS:
            th.join(0)
        return

    def start(self):
        self.s.bind(("", self.PORT))
        print("Socket binded...")
        self.s.listen()
        print("Listening...")

        while True:
            conn, addr = self.s.accept()
            th = threading.Thread(target=self.thread_handle, args=(conn,))
            th.start()
            self.THREADS.append(th)
            self.CONNS.append(conn)


beacon = NetworkBeacon(9999, "<LIVE-SERVER-MS>")
beacon.start()
# if __name__ == "__main__":
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(("", 9999))
#     print("Socket binded...")
#     s.listen()
#     print("Listening...")
#
#     while True:
#         conn, addr = s.accept()
#         th = threading.Thread(target=thread_handle, args=(conn, )).start()

