import tkinter as tk
from tkinter import Tk, Button, Frame, ttk, messagebox, END, CENTER, filedialog, Canvas
import time, threading
import os, platform, ctypes, sys, socket, urllib.request, io
from PIL import ImageTk, Image

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
PORT = 12345
stat = 0
home_score = 0
away_score = 0
home_sets = 0
away_sets = 0
home_team = "home"
away_team = "away"

# Global variable to track the Tkinter root window
root = None
home_teams= None
away_teams= None
home_scor= None
away_scor= None
home_set= None
away_set= None
serv = None

# Function to handle client connections
def handle_client_connection(client_socket, client_address):
    global root, home_score, home_sets, away_score, away_sets, home_scor, away_scor, home_teams, away_teams, home_set, away_set, home_team, away_team, serv, stat
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
                root.title("Volleyball Display")
                root.geometry("350x75")
                menu = tk.Menu(root)
                root.config(menu=menu, bg='#1476CF')
                layer = Canvas(root, width=350, height=40, bg="#0E559B", highlightthickness=0)
                layer.create_line(175, 0, 175, 999, fill='black')
                layer.pack()
                home_teams= tk.Label(root, text=f"{home_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 14))
                home_teams.place(x=87.5, y=20, anchor = CENTER, height= 20)
                away_teams= tk.Label(root, text=f"{away_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 14))
                away_teams.place(x=262.5, y=20, anchor = CENTER, height= 20)
                home_scor= tk.Label(root, text=f"Score: {home_score}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                home_scor.place(x=87.5, y=54, anchor = CENTER, height= 20)
                away_scor= tk.Label(root, text=f"Score: {away_score}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                away_scor.place(x=262.5, y=54, anchor = CENTER, height= 20)
                home_set= tk.Label(root, text=f"Sets: {away_sets}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                home_set.place(x=87.5, y=78, anchor = CENTER, height= 20)
                away_set= tk.Label(root, text=f"Sets: {away_sets}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                away_set.place(x=262.5, y=78, anchor = CENTER, height= 20)
                serv = tk.Label(root, text="<", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 16))
                serv.place(x=175, y=78, anchor = CENTER, height= 20)
                root.mainloop()
            elif data == "close":
                if root:
                    root.destroy()
                    root = None
                    print("Menu closed.")
            else:
                left = data.strip("1234567890 ")
                right = data.strip("abcdefghijklmnopqrstuvwxyz ")
                team_op = data[:2]
                team_name = data[3:]
                if stat == 1:
                    if data == "swap":
                        stat = 0
                        ball_way = "<"
                        print(stat)
                elif stat == 0:
                    if data == "swap":
                        stat = 1
                        ball_way = ">"
                        print(stat)
                if left == "vhp":
                    home_score = right
                    home_scor.config(text=f"Score: {home_score}")
                    break
                if left == "vap":
                    away_score = right
                    away_scor.config(text=f"Score: {away_score}")
                    break
                if left == "vhs":
                    home_sets = right
                    home_set.config(text=f"Sets: {home_sets}")
                    break
                if left == "vas":
                    away_sets = right
                    away_set.config(text=f"Sets: {away_sets}")
                    break
                if left == "swap":
                    serv.config(text=f"{ball_way}")
                    break
                if team_op == "Hn":
                    home_team = team_name
                    home_teams.config(text=f"{home_team}")
                    print(home_team)
                if team_op == "An":
                    away_team = team_name
                    away_teams.config(text=f"{away_team}")
                    print(away_team)
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
