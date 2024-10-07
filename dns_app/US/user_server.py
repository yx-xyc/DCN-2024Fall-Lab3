from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

# Function to query the Authoritative Server for the IP of the Fibonacci Server
def query_authoritative_server(hostname, as_ip, as_port):
    query = f"TYPE=A\nNAME={hostname}\n"
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(query.encode(), (as_ip, int(as_port)))
    response, _ = udp_socket.recvfrom(1024)
    udp_socket.close()
    
    # Parse the response
    response = response.decode('utf-8').strip().split('\n')
    if len(response) > 2 and "VALUE=" in response[2]:
        ip_address = response[2].split('=')[1].strip()
        return ip_address
    else:
        return None

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci_from_fs():
    hostname = request.args.get('hostname')  # hostname of Fibonacci Server -> the one to query
    fs_port = request.args.get('fs_port')    # port of Fibonacci Server
    number = request.args.get('number')      # number to calculate
    as_ip = request.args.get('as_ip')        # ip of Authoritative Server
    as_port = request.args.get('as_port')    # port of Authoritative Server   

    # Validate parameters
    if not (hostname and fs_port and number and as_ip and as_port):
        return "Bad Request: Missing parameters", 400
    print("Parameters are valid")

    # Query Authoritative Server to get Fibonacci Server IP
    fs_ip = query_authoritative_server(hostname, as_ip, as_port)
    if fs_ip is None:
        return f"DNS Query failed: {hostname} not found", 400
    print("DNS Query successful")

    # Send request to Fibonacci Server
    fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    response = requests.get(fs_url)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return "Failed to retrieve Fibonacci number", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
