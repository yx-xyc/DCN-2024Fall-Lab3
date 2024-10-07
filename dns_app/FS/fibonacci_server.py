from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# Utility function to calculate Fibonacci
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Register Server with Authoritative Server
def register_with_authoritative_server(hostname, ip, ttl=10):
    print("Registering with Authoritative Server")
    message = (
        f"TYPE=A\n"
        f"NAME={hostname}\n"
        f"VALUE={ip}\n"
        f"TTL={ttl}\n"
    )
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Send the registration message to Authoritative Server
    udp_socket.sendto(message.encode(), ("127.0.0.1", 53533))
    # Wait for the response from the Authoritative Server
    udp_socket.settimeout(5)  # Set a timeout of 5 seconds
    try:
        response, _ = udp_socket.recvfrom(1024)  # Wait for response from AS
        response_message = response.decode('utf-8')
        print(f"Received response from AS: {response_message}")
    except socket.timeout:
        response_message = "No response from Authoritative Server (timeout)"
    udp_socket.close()
    return response_message

# Endpoint to allow registering any hostname and IP with the AS
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input data
    hostname = data.get('hostname')
    ip = data.get('ip')
    ttl = data.get('ttl', 10)  # Default TTL is 10 if not provided

    if not hostname or not ip:
        return jsonify({"error": "hostname and ip are required"}), 400

    # Register the given hostname and IP with the Authoritative Server
    response_message =register_with_authoritative_server(hostname, ip, ttl)
    
    if "successful" in response_message:
        return jsonify({"message": f"Registered {hostname} -> {ip} with TTL={ttl}", "status": "success"}), 201
    else:
        return jsonify({"message": response_message, "status": "failure"}), 500

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    
    # Check if the number is a valid integer
    if not number or not number.isdigit():
        return "Bad Request: 'number' must be an integer", 400

    number = int(number)
    
    # Calculate the Fibonacci number
    result = fibonacci(number)
    return jsonify({"Fibonacci": result}), 200

if __name__ == '__main__':
    response_message = register_with_authoritative_server("fibonacci.com", "127.0.0.1")
    print(f"Fibonacci Server Registration: {response_message}")    
    app.run(debug=False, port=9090)  # Start Fibonacci Server on port 9090
