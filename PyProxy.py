import socket, re


g_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 ' \
          'Safari/537.36'


def get_http_body(sock, length):
    block_size = 2048
    data = bytes()
    received = 0
    total = int(length)

    while received < total:
        part = sock.recv(block_size)
        data += part
        received += len(part)

    ret_str = str(data, encoding="utf-8")
    return ret_str


def receive_http_response_body(sock, lines):
    body_size = get_content_length(lines)
    body = get_http_body(sock, body_size)
    return body


def get_content_length(lines):
    for line in lines:
        if line.startswith('Content-Length'):
            pattern = "[0-9]*$"
            regex = re.compile(pattern)
            result = re.search(regex, line)
            return result.group()


def get_response_headers(sock):
    lines = []

    while True:
        line = read_line(sock)

        if line == '\r\n' or line == '':
            break

        lines.append(line)
    return lines


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
        headers = get_response_headers(client)
        print(request_line)
        print(headers)

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