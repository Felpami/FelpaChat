import socket
import threading
import playsound
import PySimpleGUI as sg
from socket import error as SocketError
from cryptography.fernet import Fernet

font1=("Helvetica", 14)
font2=("Helvetica", 12)

layout_recv=[[sg.Multiline(size=(61,20),font=font1, disabled=True, key="TextBox")]]

layout_send=[[sg.Text('Message', font=font2), sg.InputText('Message',do_not_clear=False, font=font1, key="Message"), sg.Button("Send", font=font2, button_color="green", bind_return_key=True), sg.Button("Quit", font=font2, button_color="orange")]]

class felpa_client():
    def __init__(self, host, port, name, password_hash, password_b64, window, window_menu):
        self.host = host
        self.port = port
        self.username = name
        self.quit = False
        self.color = ""
        self.password_hash = password_hash
        self.password_b64 = password_b64
        self.window = window
        self.window_menu = window_menu

    def receive_msg(self, s, window_send):
        while True:
            try:
                msg = s.recv(1024).decode().split("[SEP]")
                if len(msg) == 3:
                    window_send["TextBox"].print(msg[0],text_color=msg[1],end='')
                    window_send["TextBox"].print(": " + msg[2])
                    if msg[0] != self.username:
                        playsound.playsound("incoming.wav", False)
                else:
                    if msg[0].startswith("[+]"):
                        window_send["TextBox"].print(msg[0], background_color='SeaGreen1', end='')
                        window_send["TextBox"].print('\n', end='')
                        playsound.playsound("connected.wav", False)
                    else:
                        window_send["TextBox"].print(msg[0], background_color='Orange', end='')
                        window_send["TextBox"].print('\n', end='')
                        playsound.playsound("error.wav", False)
                if self.quit:
                    window_send.close()
                    s.close()
                    break
            except SocketError as e:
                #print(e)
                window_send["TextBox"].print("[-] Server stopped!", background_color='Orange', end='')
                window_send["TextBox"].print('\n', end='')
                window_send["TextBox"].print("[*] Press quit or close the window.")
                playsound.playsound("error.wav", False)
                break

    def client(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((self.host,self.port))
        except SocketError as e:
            #print(e)
            return 0
        if server.recv(1024).decode() != "[OK]":
            return 1
        server.sendall(self.password_hash.encode())  # Step 2 send password
        if server.recv(1024).decode() != "[GRANTED]":
            return 2
        server.sendall(self.username.encode())  # Step 2 send username
        if server.recv(1024).decode() != "[OK_NAME]":
            return 3

        self.window_menu.close()
        self.window.close()
        self.color = server.recv(1024).decode()  # Step 3 assign color to user
        server.sendall("[OK]".encode())
        window_send = sg.Window(title=f"FelpaChat - Logged in as {self.username}", font=font2, layout=[[layout_recv, sg.VSeparator(), layout_send]], finalize=True)

        receive_t = threading.Thread(target=self.receive_msg, args=(server, window_send,), daemon=True)
        receive_t.start()

        while True:
            try:
                window_send.TKroot.focus_force()
                event, values = window_send.read()
                msg = values["Message"]
                server.sendall(msg.encode())
            except Exception as e:
                break
            if event == "Quit":
                self.quit = True
                server.sendall("[QUIT]".encode())
                break
