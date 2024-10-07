import socket
import json

DNS_FILE = 'dns_records.json'

# Load DNS records from file
def load_dns_records():
    try:
        with open(DNS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save DNS records to file
def save_dns_records(records):
    with open(DNS_FILE, 'w') as file:
        json.dump(records, file)

def start_authoritative_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('127.0.0.1', 53533))
    
    print("Authoritative Server running on port 53533...")
    
    dns_records = load_dns_records()

    while True:
        message, client_address = udp_socket.recvfrom(1024)
        message = message.decode('utf-8')
        lines = message.strip().split('\n')
        print(f"args:\n{lines}")
        if len(lines) > 2 and lines[0] == 'TYPE=A':
            if 'VALUE' in lines[2]:
                name = lines[1].split('=')[1].strip()
                ip_address = lines[2].split('=')[1].strip()
                ttl = lines[3].split('=')[1].strip()
                dns_records[name] = {"ip_address": ip_address, "ttl": ttl}
                save_dns_records(dns_records)
                udp_socket.sendto("Registration successful".encode(), client_address)
                print(f"Registered: {name} -> {ip_address}")
            else:
                udp_socket.sendto("Malformed registration request".encode(), client_address)
        elif len(lines) == 2 and lines[0] == 'TYPE=A':
            name = lines[1].split('=')[1].strip()
            if name in dns_records:
                ip_address = dns_records[name]["ip_address"]
                ttl = dns_records[name]["ttl"]
                response_message = f"TYPE=A\nNAME={name}\nVALUE={ip_address}\nTTL={ttl}\n"
                print(f"Response message:\n{response_message}")
                udp_socket.sendto(response_message.encode(), client_address)
                print(f"Resolved: {name} -> {ip_address}")
            else:
                udp_socket.sendto(f"{name} not found".encode(), client_address)
                print(f"Failed to resolve: {name}")

if __name__ == '__main__':
    start_authoritative_server()
