import socket


def read_line(sock):
    line = ""

    while True:
        c = sock.recv(1)

        if len(c) == 0:
            break

        if c[0] == 0xa:
            break
        else:
            d = str(c, encoding="utf-8")
            line += d

    return line.replace('\r', '')


class HttpProxy(object):

    def __init__(self, port):
        self.__port__ = port

    def handle_request(self, client):
        request_line = read_line(client)
        print(request_line)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', self.__port__))
        sock.listen(5)

        while True:
            connection, address = sock.accept()
            self.handle_request(connection)
            connection.close()


def main():
    server = HttpProxy(9999)
    print("Started http server ...")
    server.run()


if __name__ == '__main__':
    main()