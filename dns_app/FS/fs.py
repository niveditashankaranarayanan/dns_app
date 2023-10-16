import socket
from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/register', methods=['PUT'])
def register():
    try:
        req_data = request.get_json()
        print(req_data)
        asIp = req_data["as_ip"]
        asPort = int(req_data["as_port"])
        fs_req_data = {'TYPE': 'A', 'Hostname': req_data['hostname'], 'VALUE': req_data['ip'], 'TTL': 10}
        bytes = str.encode(str(fs_req_data))
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.sendto(bytes, (asIp, asPort))
        as_response = udp_socket.recvfrom(1024)
        as_response_message = "Message: {}".format(as_response[0])
        return jsonify({'response data': as_response_message}), 201
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')

    if number is None:
        return jsonify({'error': 'Missing sequence number'}), 400

    try:
        sequence_number = int(number)
        result = calculate_fibonacci(sequence_number)
        return jsonify({'Calculated Fibonacci': result}), 200
    except ValueError:
        return jsonify({'error': 'Invalid sequence number format'}), 400


def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


if __name__ == '__main__':
    app.run(debug=True, port=9090)