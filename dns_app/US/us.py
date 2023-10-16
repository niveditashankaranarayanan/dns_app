import urllib.request
import socket
from flask import Flask
from flask import request, jsonify
import ast
#!/usr/bin/env python3

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fsPort = request.args.get('fs_port')
    fsPort_int = int(fsPort)
    number = request.args.get('number')
    number_int = int(number)
    asIp = request.args.get('as_ip')
    asPort = request.args.get('as_port')
    asPort_int = int(asPort)
    req_obj = {"Type": "A", "Hostname": hostname}

    if hostname is not None and fsPort_int is not None and number_int is not None and asPort_int is not None and asIp is not None:
        bytes = str.encode(str(req_obj))
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(bytes,(asIp, asPort_int))
        response_as = udp_socket.recvfrom(1024)
        response_message = "Message: {}".format(response_as[0])
        print(response_message)
        fs_infos = response_as[0].decode("utf-8")
        print("received ip address")
        fs_info = ast.literal_eval(fs_infos)
        fs_ip = str(fs_info['VALUE'])
        request_string = "http://" + fs_ip + ":" + str(fsPort_int) + "/fibonacci?number=" + str(number)
        response_answer = urllib.request.urlopen(
            request_string)
        return response_answer, 200

    else:
        return jsonify({'error': 'Request is missing a paramater'}), 400

if __name__ == '__main__':
    app.run(debug=True,port=8080)