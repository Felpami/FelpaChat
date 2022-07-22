import socket
import threading
import playsound
import PySimpleGUI as sg
from socket import error as SocketError
from Crypto.Cipher import AES

font1=("Helvetica", 14)
font2=("Helvetica", 12)

class felpa_client():
    def __init__(self, host, port, username, password_hash, window, window_menu):
        self.host = host
        self.port = port
        self.username = username
        self.username_a = []
        self.user_color_a = []
        self.color = ""
        self.password_hash = password_hash
        self.window = window
        self.window_menu = window_menu

    def enc(self, msg):
        cipher = AES.new(self.password_hash, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode("latin-1"))
        return ciphertext+b"..."+cipher.nonce

    def dec(self, msg):
        ar = msg.decode("latin-1").split("...")
        cipher = AES.new(self.password_hash, AES.MODE_EAX, nonce=ar[1].encode("latin-1"))
        return cipher.decrypt(ar[0].encode("latin-1")).decode("latin-1")

    def user_list_update(self, window_send):
        window_send["ListBox"].update("")
        i = 0
        for user in self.username_a:
            #window_send["ListBox"].print(user, text_color=self.user_color_a[self.username_a.index(user)])
            window_send["ListBox"].print(user, text_color=self.user_color_a[i])
            i += 1

    def receive_msg(self, s, window_send):
        while True:
            try:
                msg = self.dec(s.recv(1024)).split("[SEP]")
                if len(msg) == 3:
                    window_send["TextBox"].print(msg[0],text_color=msg[1],end='')
                    window_send["TextBox"].print(": " + msg[2])
                    if msg[0] != self.username:
                        playsound.playsound("incoming.wav", False)
                else:
                    if msg[0].startswith("[+]"):
                        window_send["TextBox"].print(msg[0], background_color='SeaGreen1', end='')
                        window_send["TextBox"].print('\n', end='')
                        user = msg[0].split(" ")[1]
                        self.username_a.append(user)
                        self.user_color_a.append(msg[1])
                        self.user_list_update(window_send)
                        playsound.playsound("connected.wav", False)
                    else:
                        window_send["TextBox"].print(msg[0], background_color='Orange', end='')
                        window_send["TextBox"].print('\n', end='')
                        user = msg[0].split(" ")[1]
                        if user in self.username_a:
                            self.user_color_a.remove(self.user_color_a[self.username_a.index(user)])
                            self.username_a.remove(user)
                        self.user_list_update(window_send)
                        playsound.playsound("error.wav", False)
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
        m = self.dec(server.recv(1024))
        if m != "[OK]":
            return 1
        #server.sendall(self.password_hash.encode())  # Step 2 send password
        server.sendall(self.enc(self.password_hash.decode("latin-1")))
        if self.dec(server.recv(1024)) != "[GRANTED]":
            return 2
        server.sendall(self.enc(self.username))
        if self.dec(server.recv(1024)) != "[OK_NAME]":
            return 3

        while True:
            msg = self.dec(server.recv(1024)).split("[SEP]")
            if msg[0] == "[END]":
                break
            else:
                self.username_a.append(msg[0])
                self.user_color_a.append(msg[1])
                server.sendall(self.enc("[OK]"))
        self.color = self.dec(server.recv(1024))
        layout_recv = [[sg.Multiline(size=(67, 20), font=font1, disabled=True, key="TextBox"),
                        sg.Multiline(size=(17, 20), font=font1, disabled=True, key="ListBox")]]
        layout_send = [
            [sg.Text('Message', font=font2),
             sg.InputText('Message', do_not_clear=False, font=font1, key="Message", size=(61, 1)),
             sg.Button("Send", font=font2, button_color="green", bind_return_key=True, size=(10, 1)),
             sg.Button("Quit", font=font2, button_color="orange", size=(10, 1))]]
        self.window_menu.close()
        self.window.close()
        window_send = sg.Window(title=f"FelpaChat - Logged in as {self.username}", font=font2, layout=[[layout_recv, sg.VSeparator(), layout_send]], finalize=True)
        window_send.TKroot.focus_force()
        receive_t = threading.Thread(target=self.receive_msg, args=(server, window_send,), daemon=True)
        receive_t.start()
        while True:
            try:
                event, values = window_send.read()
                if event == "Quit" or event == sg.WINDOW_CLOSED:
                    server.sendall(self.enc("[QUIT]"))
                    break
                else:
                    msg = values["Message"]
                    if "[SEP]" in msg:
                        window_send["TextBox"].print("Cannot send message with keyword '[SEP]'.")
                    elif len(msg) != 0:
                        server.sendall(self.enc(msg))
            except (SocketError, Exception) as e:
                print(e)
                break
