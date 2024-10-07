# DNC-2024Fall-Lab3

# AS
# Register a hostname and IP with the AS using the /register endpoint
# Query the Authoritative Server to get the IP address of the Fibonacci Server

# US
# Firstly, use input parameter to fetch the IP address of the Fibonacci Server from the Authoritative Server
# Then, Query the Fibonacci number from the Fibonacci Server using the /fibonacci endpoint

# Test to query the Fibonacci number from User Server 
# which fetches the IP address of the Fibonacci Server from Authoritative Server 
# and then fetches the Fibonacci number from the Fibonacci Server
```bash
curl "http://localhost:8080/fibonacci?hostname=example.com&fs_port=9090&number=10&as_ip=127.0.0.1&as_port=53533"
```

# FS
# Register itself with the AS, using the /register endpoint.
# Register a hostname and IP with the AS with a TTL.
# Server as the Fibonacci Server
# Calculate the Fibonacci number using the /fibonacci endpoint
# Test to register a hostname and IP with the AS
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"hostname": "example.com", "ip": "192.168.1.10", "ttl": 20}' \
http://localhost:9090/register
```