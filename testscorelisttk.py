import tkinter as tk
from tkinter import Tk, Button, Frame, ttk, messagebox, END, CENTER, filedialog
import time
import os, platform, ctypes, sys, socket

teams = ['HHS Lakers', 'SVHS Vikings', 'FCA Eagles', 'CICS Vikings', 'CRHS Tigers', 'WS Tunder', 'Mc Warriors', 'SRS Cougars', 'JCS Golden Knights', 'Fundy Mariners', 'HCS Huskies', 'VCA Eagles']
files = 0
volley_sets_home = 0
volley_sets_away = 0
volley_score_home = 0
volley_score_away = 0
home_team = "Home"
away_team = "Away"
ser = home_team
v_h_p_i = 'q' 
v_h_p_d = 'w'
v_a_p_i = 'r'
v_a_p_d = 't'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name 

host = socket.gethostname() 

port = 9999 

# bind socket to public host, and a port 

serversocket.bind((host, port)) 

# become a server socket 

serversocket.listen(5) 
 

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def Checks_files(file_paths):
    global files, teams
    for file_path in file_paths:
        directory = os.path.dirname(file_path)
        if file_path == f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams":
            if not os.path.exists(file_path):
                if is_admin():
                    os.makedirs(directory, exist_ok=True)
                    print("Created folder at", directory)
                else:
                    print("Please run the script as an administrator to create this folder.")
                    if not hasattr(sys, 'frozen'):
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    return
            else:
                print("The folder already exists at", directory)


        if file_path != f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams":
            if not os.path.exists(file_path):
                if is_admin():
                    os.makedirs(directory, exist_ok=True)
                    with open(file_path, "w") as file:
                        for team in teams:
                            file.write(team+"\n")
                else:
                    print("Please run the script as an administrator to create this file.")
                    if not hasattr(sys, 'frozen'):
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    return
            else:
                print("Note file already exists at", file_path)
    files += 2


file_paths = [
    f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams",
    f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt"
]

Checks_files(file_paths)

#functions are used in the team config tab
def add_new_teams(i, l):
    team = i.get()
    if team != "":
        i.delete(0, END)
        l.delete(0, END)
        file = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r+')
        file.write(team+ "\n")
        Lines = file.readlines()
        curret_line = 0
        file.close()
        file = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r+')
        Lines = file.readlines()
        curret_line = 0
        l.delete(0, END)
        for line in Lines:
            curret_line += 1
            l.insert(curret_line, line.strip())
        file.close()

def remove_new_teams(l):
    team = l.get(l.curselection())
    if team != "":
        l.delete(0, END)
        file = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r')
        lines = file.readlines()
        file = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'w')
        for line in lines:
            if line.strip("\n") != team:
                file.write(line)
        file.close()
        file = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r+')
        Lines = file.readlines()
        curret_line = 0
        l.delete(0, END)
        for line in Lines:
            curret_line += 1
            l.insert(curret_line, line.strip())
        file.close()


#functions are used in the volleyball scoreboard tab
def reset_score_board(h, a, hs, aws):
    global volley_score_home, volley_score_away, home_team, away_team
    volley_score_home = 0
    volley_score_away = 0
    home_team = "home"
    away_team = "away"
    h.config(text =f"{home_team} {volley_score_home}")
    a.config(text=f"{away_team} {volley_score_away}")

def reset_score_home(h):
    global volley_score_home, home_team
    volley_score_home = 0
    h.config(text =f"{home_team} {volley_score_home}")

def reset_score_away(a):
    global volley_score_away, away_team
    volley_score_away = 0
    a.config(text=f"{away_team} {volley_score_away}")

def home_score_dis(i, h):
    global volley_score_home
    if i == 2:
        if volley_score_home < 99:
            volley_score_home += 1
            server("vbhp", "+")
        h.config(text =f"{home_team} {volley_score_home}")
    else:
        if volley_score_home > 0:
            volley_score_home -= 1
            server("vbhp", "+")
        h.config(text =f"{home_team} {volley_score_home}")

def away_score_dis(i , a):
    global volley_score_away
    if i == 2:
        if volley_score_away < 99:
            volley_score_away += 1
            server("vbap", "+")
        a.config(text=f"{away_team} {volley_score_away}")
    else:
        if volley_score_away > 0:
            volley_score_away -= 1
            server("vbap", "-")
        a.config(text=f"{away_team} {volley_score_away}")

def home_sets(i, h):
    global volley_sets_home
    if i == 2:
        if volley_sets_home < 9:
            volley_sets_home += 1
            server("vbhs", "+")
        h.config(text=f"{volley_sets_home} sets")
    else:
        if volley_sets_home > 0:
            volley_sets_home -= 1
            server("vbhs", "+")
        h.config(text=f"{volley_sets_home} sets")

def away_sets(i, h):
    global volley_sets_away
    if i == 2:
        if volley_sets_away < 9:
            volley_sets_away += 1
            server("vbas", "+")
        h.config(text=f"{volley_sets_away} sets")
    else:
        if volley_sets_away > 0:
            volley_sets_away -= 1
            server("vbas", "+")
        h.config(text=f"{volley_sets_away} sets")

def serving(i, s, h, a):
    global ser, away_team, home_team
    if i == 2:
        if ser != home_team:
            ser = home_team
            server("vbsv", "home")
        s.config(text=f"{ser} is serving")
        a["state"] = "normal"
        h["state"] = "disable"
    else:
        if ser != away_team:
            ser = away_team
            server("vbsv", "away")
        s.config(text=f"{ser} is serving")
        h["state"] = "normal"
        a["state"] = "disable"


def set_home_team(h, i, v, s):
    global home_team, ser, away_team
    savename = away_team
    if ser == home_team:
        home_team = i.get(i.curselection())
        if home_team != away_team:
            h.config(text =f"{home_team} {volley_score_home}")
            ser = home_team
            s.config(text=f"{ser} is serving")
        else:
            away_team = savename
    else:
        home_team = i.get(i.curselection())
        if home_team != away_team:
            h.config(text =f"{home_team} {volley_score_home}")
        else:
            away_team = savename
    v.focus_set()
    server("vbhn")

def set_away_team(a, i, v, s):
    global away_team, ser, home_team
    savename = away_team
    if ser == away_team:
        away_team = i.get(i.curselection())
        if away_team != home_team:
            a.config(text=f"{away_team} {volley_score_away}")
            ser = away_team
            s.config(text=f"{ser} is serving")
        else:
            away_team = savename
    else:
        away_team = i.get(i.curselection())
        if away_team != home_team:
            a.config(text=f"{away_team} {volley_score_away}")
        else:
            away_team = savename
    v.focus_set()
    server("vban")

def server (w , s):
    message = ""
    # establish a connection 
    clientsocket, addr = serversocket.accept() 
    print ("Got a connection from %s" % str(addr)) 
    if w == "vbhp":
        if s == "+":
            message = "vbhpp"
        if s == "-":
            message = "vbhpn"
    if w == "vbap":
        if s == "+":
            message = "vbapp"
        if s == "-":
            message = "vbapn"
    if w == "vbhs":
        if s == "+":
            message = "vbhsp"
        if s == "-":
            message = "vbhsn"
    if w == "vbas":
        if s == "+":
            message = "vbasp"
        if s == "-":
            message = "vbasn"
    if w == "vbsv":
        if s == "home":
            message = "vbsvh"
        if s == "away":
            message = "vbsva"
    if w == "vbhn":
        message = w
    if w == "vban":
        message = w
    clientsocket.send(message.encode('ascii')) 
    # close the client connection 
    clientsocket.close()


    
def main():
    root = tk.Tk()
    root.title("Scoreboard_controller")
    root.geometry("250x150")
    root.config(bg='#36393e')

    title_label = tk.Label(root, text="Please pick a scoreboard to use")
    title_label.place(x=45, y=30)

    volleyball_button = tk.Button(root, text="Volleyball", command=show_volleyball_scoreboard)
    volleyball_button.place(x=30, y=90)

    basketball_button = tk.Button(root, text="Basketball", command=show_basketball_scoreboard)
    basketball_button.place(x=30, y=60)

    Teams_config = tk.Button(root, text="Teams configs", command=Teams_configs)
    Teams_config.place(x=110, y=60)

    root.mainloop()

def Teams_configs():
    Teams_configs = tk.Toplevel()
    Teams_configs.title("Teams configs")
    Teams_configs.geometry("300x250")
    Teams_configs.focus_set()
    Teams_configs.config(bg='#36393e')

    back_button = tk.Button(Teams_configs, text="Back", command=Teams_configs.destroy)
    back_button.place(x=30, y=230, anchor = CENTER)

    team_input = tk.Button(Teams_configs, text="input team name", command = lambda: add_new_teams(team_name_input, team_list))
    team_input.place(x=60, y=60, anchor = CENTER)

    team_input = tk.Button(Teams_configs, text="deleted selected team", command = lambda: remove_new_teams(team_list))
    team_input.place(x=72, y=110, anchor = CENTER)

    team_name_input = tk.Entry(Teams_configs, width = 23)
    team_name_input.place(x=80, y=30, anchor = CENTER)

    team_list = tk.Listbox(Teams_configs, height= 13)
    team_list.place(x=225, y=125, anchor = CENTER)

    info = tk.Label(Teams_configs, text="please make sure after \n deleteing/adding a team you \n reopen the volleyball \n or baskebal tab", width = 23, bg='#36393e', fg='#FFFFFF')
    info.place(x=80, y=170, anchor = CENTER)

    file1 = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r')
    Lines = file1.readlines()
    curret_line = 0
    for line in Lines:
        curret_line += 1
        team_list.insert(curret_line, line.strip())

def show_volleyball_scoreboard():
    volleyball_frame = tk.Toplevel()
    volleyball_frame.title("Scoreboard controller")
    volleyball_frame.geometry("800x600")
    volleyball_frame.focus_set()
    volleyball_frame.config(bg='#36393e')
    setting = 2

    back_button = tk.Button(volleyball_frame, text="Back", command=volleyball_frame.destroy)
    back_button.place(x=25, y=510)

    full_reset_button = tk.Button(volleyball_frame, text="Reset Scoreboard", command = lambda: reset_score_board(home_score, away_score), font=(26))
    full_reset_button.place(x=620, y=490, width = 150, height = 75)

    home_increase_button = tk.Button(volleyball_frame, text="+", command = lambda: home_score_dis(setting, home_score))  
    home_increase_button.place(x=78, y=100, width=75, height = 50, anchor = CENTER)

    home_decrease_button = tk.Button(volleyball_frame, text="-", command = lambda: home_score_dis("filler", home_score))
    home_decrease_button.place(x=242, y=100, width=75, height = 50, anchor = CENTER)

    away_increase_button = tk.Button(volleyball_frame, text="+", command = lambda: away_score_dis(setting, away_score))
    away_increase_button.place(x=378, y=100, width=75, height = 50, anchor = CENTER)

    away_decrease_button = tk.Button(volleyball_frame, text="-", command = lambda: away_score_dis("filler", away_score))
    away_decrease_button.place(x=542, y=100, width=75, height = 50, anchor = CENTER)

    home_reset_button = tk.Button(volleyball_frame, text="Reset Score", command = lambda: reset_score_home(home_score))
    home_reset_button.place(x=160, y=115, width = 70, height = 40, anchor = CENTER)

    away_reset_button = tk.Button(volleyball_frame, text="Reset Score", command = lambda: reset_score_away(away_score))
    away_reset_button.place(x=460, y=115, width = 70, height = 40, anchor = CENTER)

    home_score = tk.Label(volleyball_frame, text=f"{home_team} {volley_score_home}", bg='#36393e', fg='#FFFFFF', font=(26))
    home_score.place(x=160, y=55, anchor = CENTER)

    away_score = tk.Label(volleyball_frame, text=f"{away_team} {volley_score_away}", bg='#36393e', fg='#FFFFFF', font=(26))
    away_score.place(x=460, y=55, anchor = CENTER)

    home_setI_button = tk.Button(volleyball_frame, text="+", command = lambda: home_sets(setting, home_set))  
    home_setI_button.place(x=78, y=225, width=75, height = 50, anchor = CENTER)

    home_setD_button = tk.Button(volleyball_frame, text="-", command = lambda: home_sets("filler", home_set))
    home_setD_button.place(x=242, y=225, width=75, height = 50, anchor = CENTER)

    away_setI_button = tk.Button(volleyball_frame, text="+", command = lambda: away_sets(setting, away_set))
    away_setI_button.place(x=378, y=225, width=75, height = 50, anchor = CENTER)

    away_setD_button = tk.Button(volleyball_frame, text="-", command = lambda: away_sets("filler", away_set))
    away_setD_button.place(x=542, y=225, width=75, height = 50, anchor = CENTER)

    home_set = tk.Label(volleyball_frame, text=f"{volley_sets_home} sets", bg='#36393e', fg='#FFFFFF', font=(26))
    home_set.place(x=160, y=190, anchor = CENTER)

    away_set = tk.Label(volleyball_frame, text=f"{volley_sets_away} sets", bg='#36393e', fg='#FFFFFF', font=(26))
    away_set.place(x=460, y=190, anchor = CENTER)

    home_team_choose = tk.Button(volleyball_frame, text="input selected\nhome team", command = lambda: set_home_team(home_score, home_list, volleyball_frame, serve), height = 2)
    home_team_choose.place(x=275, y=525, anchor = CENTER)

    away_team_choose = tk.Button(volleyball_frame, text="input selected\naway team", command = lambda: set_away_team(away_score, away_list, volleyball_frame, serve), height = 2)
    away_team_choose.place(x=525, y=525, anchor = CENTER)

    home_list = tk.Listbox(volleyball_frame, height= 11)
    home_list.place(x=100, y=400)

    away_list = tk.Listbox(volleyball_frame, height= 11)
    away_list.place(x=345, y=400)

    serving_home = tk.Button(volleyball_frame, text="Home serve", command = lambda: serving(setting, serve, serving_home, serving_away))
    serving_home.place(x=160, y=325, width=75, height = 50, anchor = CENTER)
    serving_home["state"] = "disable"

    serving_away = tk.Button(volleyball_frame, text="Away serve", command = lambda: serving("filler", serve, serving_home, serving_away))
    serving_away.place(x=460, y=325, width=75, height = 50, anchor = CENTER)

    serve = tk.Label(volleyball_frame, text=f"{ser} is serving", bg='#36393e', fg='#FFFFFF', font=(50))
    serve.place(x=310, y=325, anchor = CENTER)

    file1 = open(f"c:/Users/{os.getenv('USERNAME')}/OneDrive/Documents/Scoreboard_saved_teams/team.txt", 'r')
    Lines = file1.readlines()
    curret_line = 0
    for line in Lines:
        curret_line += 1
        home_list.insert(curret_line, line.strip())
        away_list.insert(curret_line, line.strip())
    
    volleyball_frame.bind(v_h_p_i, lambda event: home_increase_button.invoke())
    volleyball_frame.bind(v_h_p_d, lambda event: home_decrease_button.invoke())
    volleyball_frame.bind(v_a_p_i, lambda event: away_increase_button.invoke())
    volleyball_frame.bind(v_a_p_d, lambda event: away_decrease_button.invoke())

        

    


def show_basketball_scoreboard():
    basketball_frame = tk.Toplevel()
    basketball_frame.title("Scoreboard_controller")
    basketball_frame.geometry("800x600")
    basketball_frame.config(bg='#36393e')

    back_button = tk.Button(basketball_frame, text="Back", command=basketball_frame.destroy)
    back_button.place(x=25, y=510)

    basketball_frame.focus_set()

if __name__ == "__main__":
    if files >= 2:
        main()
    

