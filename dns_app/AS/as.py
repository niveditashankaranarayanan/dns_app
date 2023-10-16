import socket
import ast
from flask import Flask, abort

app = Flask(__name__)

asIP = "127.0.0.1"
asPort = 53534

def udp_socket_code(asIP, asPort):
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind((asIP, asPort))
    return udp_socket

def fs_body(asIP, asPort):
    udp_socket = udp_socket_code(asIP, asPort)
    asResponse = "Authoritative Server has registered Fibonacci Server"
    bytes = str.encode(asResponse)
    while True:
        response_bytes = udp_socket.recvfrom(1024)
        print(response_bytes[0], response_bytes[1])
        udp_socket.sendto(bytes, response_bytes[1])
        return response_bytes[0]

def us_response(asIP, asPort):
    udp_socket = udp_socket_code(asIP, asPort)
    while True:
        bytes = udp_socket.recvfrom(1024)
        return bytes[0], bytes[1], udp_socket

def dns_lookup(fs_obj, us_obj):
    us_obj = ast.literal_eval(str(us_obj, encoding='utf-8'))
    fs_obj = ast.literal_eval(str(fs_obj, encoding='utf-8') )
    if us_obj['Type'] == fs_obj['TYPE'] and us_obj['Hostname'] == fs_obj['Hostname']:
        return 200
    else:
        return 404

def response_us_server(us_response, status_code, fs_obj):
    print(us_response[1], us_response[2])
    address = us_response[1]
    udp_socket = us_response[2]
    if status_code == 200:
        response_as = str(fs_obj.decode('utf-8'))
        bytes = str.encode(response_as)
        udp_socket.sendto(bytes, address)
        return "Success", 200
    else:
        abort(400)



if __name__ == '__main__':
    while True:
        FS_obj = fs_body(asIP, asPort)
        US_Values = us_response(asIP, asPort)
        US_obj = US_Values[0]
        check_val = dns_lookup(FS_obj, US_obj)
        response_us_server(US_Values, check_val, FS_obj)
