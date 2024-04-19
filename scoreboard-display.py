import socket
import threading
import tkinter as tk

def get_ipv4_address():
    # Create a temporary socket to get the local IP address
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to any remote address (doesn't have to be reachable)
        temp_socket.connect(("8.8.8.8", 80))
        # Get the local IP address connected to the socket
        ip_address = temp_socket.getsockname()[0]
    finally:
        temp_socket.close()
    return ip_address

# Define the host and port on which the server will listen
HOST = get_ipv4_address()
PORT = 65432

# Global variable to track the Tkinter root window
root = None

# Function to handle client connections
def handle_client_connection(client_socket, client_address):
    global root

    print(f"Connection established with {client_address}")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        if not data:
            print("No data received. Closing connection.")
            break
        else:
            print(f"Received message from client {client_address}: {data}")
            # Check if received data triggers displaying the Tkinter menu
            if data == "volley":
                # Create and display a Tkinter menu
                root = tk.Tk()
                root.title("Server Menu")

                menu = tk.Menu(root)
                root.config(menu=menu)

                root.mainloop()
            break

    # Close the connection with the client
    client_socket.close()
    print(f"Connection with {client_address} closed.")

# Function to start the server and listen for incoming connections
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        
        # Handle the client connection in a new thread
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()

# Start the server
if __name__ == "__main__":
    start_server()
