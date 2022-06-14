import socket
import time

IP = "3.126.224.214"
PORT = 13080
ADDR=(IP,PORT)
FORMAT = "utf-8"
SIZE = 1024
while True:
    def main():

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        client.connect(ADDR)


        file = open("signal.txt", "r")
        data = file.read()


        client.send("signal.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")


        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")


        file.close()


        client.close()
        time.sleep(2)

    if __name__ == "__main__":
        main()