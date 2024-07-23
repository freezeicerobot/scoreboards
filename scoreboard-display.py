import tkinter as tk
from tkinter import Tk, Button, Frame, ttk, messagebox, END, CENTER, filedialog, Canvas
import os, platform, ctypes, sys, socket, urllib.request, io, time, datetime, threading

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
home_fouls = 0
away_fouls = 0
home_timeouts = 0
away_timeouts = 0
quarters = 1
timer = [600]
timer_running = [False]

# Global variable to track the Tkinter root window
root = None
home_teams= None
away_teams= None
home_scor= None
away_scor= None
home_set= None
away_set= None
serv = None
home_foul = None
away_foul = None
home_timeout = None
away_timeout = None
quarter = None
times = None
home_bonus = None
away_bonus = None

# Function to handle client connections
def handle_client_connection(client_socket, client_address):
    global root, home_score, home_sets, away_score, away_sets, home_scor, away_scor, home_teams, away_teams, home_set, away_set, home_team, away_team, serv, stat, quarters, away_timeouts, home_timeouts, away_fouls, home_fouls, quarter, away_timeout, home_timeout, away_foul, home_foul, timer, times, away_bonus, home_bonus
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
                home_teams= tk.Label(root, text=f"{home_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 13))
                home_teams.place(x=87.5, y=20, anchor = CENTER, height= 20)
                away_teams= tk.Label(root, text=f"{away_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 13))
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
            elif data == "basket":
                # Create and display a Tkinter menu
                root = tk.Tk()
                root.title("Basket Display")
                root.geometry("400x50")
                menu = tk.Menu(root)
                root.config(menu=menu, bg='#1476CF')
                layer = Canvas(root, width=350, height=40, bg="#0E559B", highlightthickness=0)
                layer.create_line(175, 0, 175, 999, fill='black')
                layer.pack()
                layer.place(x=175, y=20, anchor = CENTER)
                home_teams = tk.Label(root, text=f"{home_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 13))
                home_teams.place(x=87.5, y=20, anchor = CENTER, height=20)
                away_teams = tk.Label(root, text=f"{away_team}", bg='#0E559B', fg='#FFFFFF', font=('DejaVu Sans', 13))
                away_teams.place(x=262.5, y=20, anchor = CENTER, height=20)
                defider = tk.Label(root, text=f"-", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 13))
                defider.place(x=175, y=54, anchor = CENTER, height=20)
                home_scor = tk.Label(root, text=f"{home_score}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                home_scor.place(x=155, y=54, anchor = CENTER, height=20)
                away_scor = tk.Label(root, text=f"{away_score}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                away_scor.place(x=195, y=54, anchor = CENTER, height=20)
                home_foul = tk.Label(root, text=f"Fouls: {home_fouls}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 10))
                home_foul.place(x=35, y=54, anchor = CENTER, height=20)
                away_foul = tk.Label(root, text=f"Fouls: {away_fouls}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 10))
                away_foul.place(x=240, y=54, anchor = CENTER, height=20)
                home_timeout = tk.Label(root, text=f"Timeout: {home_timeouts}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 10))
                home_timeout.place(x=100, y=54, anchor = CENTER, height=20)
                away_timeout = tk.Label(root, text=f"Timeout: {away_timeouts}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 10))
                away_timeout.place(x=305, y=54, anchor = CENTER, height=20)
                times = tk.Label(root, text=f"10:00", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                times.place(x=375, y=20, anchor = CENTER, height=20)
                quarter = tk.Label(root, text=f"Q: {quarters}", bg='#1476CF', fg='#FFFFFF', font=('DejaVu Sans', 12))
                quarter.place(x=375, y=54, anchor = CENTER, height=20)
                home_bonus = tk.Label(root, text="B", bg='#FF0000', fg='#FFFFFF', font=(13))
                away_bonus = tk.Label(root, text="B", bg='#FF0000', fg='#FFFFFF', font=(13))
                update_display(times)
                root.mainloop()
            elif data == "close":
                if root:
                    root.destroy()
                    root = None
                    print("Menu closed.")
            else:
                left = data.strip("1234567890[] ")
                right = data.strip("abcdefghijklmnopqrstuvwxyz[] ")
                team_op = data[:2]
                team_name = data[3:]
                print(left)
                print(right)
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
                    if len(home_team) > 16:
                        home_teams.config(text=f"{home_team}", font=('DejaVu Sans', 11))
                    else:
                        home_teams.config(text=f"{home_team}", font=('DejaVu Sans', 13))
                if team_op == "An":
                    away_team = team_name
                    if len(away_team) > 16:
                        away_teams.config(text=f"{away_team}", font=('DejaVu Sans', 11))
                    else:
                        away_teams.config(text=f"{away_team}", font=('DejaVu Sans', 13))
                if left == "bhp":
                    home_score = right
                    home_scor.config(text=f"{home_score}")
                    break
                if left == "bap":
                    away_score = right
                    away_scor.config(text=f"{away_score}")
                    break
                if left == "hf":
                    home_fouls = right
                    t = int(home_fouls)
                    if t >= 5:
                        home_bonus.place(x=341, y=28, anchor = CENTER)
                    else:
                        home_bonus.place_forget()
                    home_foul.config(text=f"Fouls: {home_fouls}")
                    break
                if left == "af":
                    away_fouls = right
                    t = int(away_fouls)
                    if t >= 5:
                        away_bonus.place(x=5, y=28, anchor = CENTER)
                    else:
                        away_bonus.place_forget()
                    away_foul.config(text=f"Fouls: {away_fouls}")
                    break
                if left == "ht":
                    home_timeouts = right
                    home_timeout.config(text=f"Timeout: {home_timeouts}")
                    break
                if left == "at":
                    away_timeouts = right
                    away_timeout.config(text=f"Timeout: {away_timeouts}")
                    break
                if left == "q":
                    quarters = right
                    t = int(quarters)
                    if t >= 5:
                        quarter.config(text=f"OQ: {quarters}")
                    else:
                        quarter.config(text=f"Q: {quarters}")
                    break
                if left == "start":
                    clocktimer (2, times)
                    break
                if left == "stop":
                    clocktimer ("filler", times)
                    break
                if left == "clock":
                    settime (times, right)
            break
    # Close the connection with the client
    client_socket.close()
    print(f"Connection with {client_address} closed.")

def settime (t, s):
    global timer
    timer[0] = int(s)
    update_timer(t)
    update_display(t)

def clocktimer (m, t):
    global timer_running, timer
    if m == 2:
        if not timer_running[0]:
            timer_running[0] = True
            update_timer(t)
            update_display(t)
    else:
        timer_running[0] = False
        update_display(t)

def update_timer(t):
    global timer_running, timer
    if timer_running[0] and timer[0] > 0:
        timer[0] -= 1
        update_display(t)
        t.after(1000, update_timer, t)

def update_display(t):
    global timer
    minutes, seconds = divmod(timer[0], 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    t.config(text=time_str)

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
    print("version 6")
