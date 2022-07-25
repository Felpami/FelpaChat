import socket
import threading
import playsound
import PySimpleGUI as sg
import base64
from socket import error as SocketError
from Crypto.Cipher import AES

font1=("Helvetica", 14)
font2=("Helvetica", 12)
SIZE = 512

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
        self.quit = False

    def popup(self, str):
        layout_popup = [[sg.Text(str)], [sg.Button("Exit", key="Exit", size=(13, 1), button_color="orange")]]
        layout = [[sg.Column(layout_popup, element_justification="c")]]
        window_popup = sg.Window(title="Error", font=font2, layout=layout, finalize=True, icon='./image/icon.ico')
        window_popup.TKroot.focus_force()
        window_popup.read(close=True)

    def enc(self, msg):
        cipher = AES.new(self.password_hash, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode("latin-1"))
        return base64.b64encode(ciphertext+b"[SEP]"+cipher.nonce)

    def dec(self, msg):
        ar = base64.b64decode(msg).decode("latin-1").split("[SEP]")
        if len(ar) == 2:
            cipher = AES.new(self.password_hash, AES.MODE_EAX, nonce=ar[1].encode("latin-1"))
            return cipher.decrypt(ar[0].encode("latin-1")).decode("latin-1")
        else:
            print("Error")
            return "Error"

    def user_list_update(self, window_send):
        window_send["ListBox"].update("")
        i = 0
        for user in self.username_a:
            #window_send["ListBox"].print(user, text_color=self.user_color_a[self.username_a.index(user)])
            window_send["ListBox"].print(user, text_color=self.user_color_a[i])
            i += 1

    def receive_msg(self, s, window_send):
        while True:
            msg = ""
            try:
                msg = self.dec(s.recv(SIZE)).split("[SEP]")
            except SocketError as e:
                #print(e)
                if (not self.quit):
                    window_send["TextBox"].print("Server stopped", text_color='red')
                    window_send["TextBox"].print("Press quit or close the window")
                    playsound.playsound("error.wav", False)
                break
            if len(msg) == 3:
                window_send["TextBox"].print(msg[0],text_color=msg[1],end='')
                window_send["TextBox"].print(": " + msg[2])
                if msg[0] != self.username:
                    playsound.playsound("incoming.wav", False)
            else:
                if "connected" in msg[0]:
                    window_send["TextBox"].print(msg[0], text_color='green')
                    user = msg[0].split(" ")[0]
                    self.username_a.append(user)
                    self.user_color_a.append(msg[1])
                    self.user_list_update(window_send)
                    playsound.playsound("connected.wav", False)
                else:
                    window_send["TextBox"].print(msg[0], text_color='Orange')
                    user = msg[0].split(" ")[0]
                    if user in self.username_a:
                        self.user_color_a.remove(self.user_color_a[self.username_a.index(user)])
                        self.username_a.remove(user)
                    self.user_list_update(window_send)
                    playsound.playsound("error.wav", False)

    def client(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((self.host, self.port))
            response = self.dec(server.recv(SIZE))
            if response == "[OK]":
                server.sendall(self.enc(self.username))
                if self.dec(server.recv(SIZE)) != "[OK_NAME]":
                    server.close()
                    return 3
            elif response == "[FULL]":
                server.close()
                return 1
            else:
                server.close()
                return 2
            #server.sendall(self.enc(self.password_hash.decode("latin-1")))
            #if self.dec(server.recv(SIZE)) != "[GRANTED]":
            #    return 2
        except SocketError as e:
            #print(e)
            #self.popup("Cannot contact server, retry.")
            return 0
        while True:
            try:
                msg = self.dec(server.recv(SIZE)).split("[SEP]")
            except SocketError as e:
                #print(e)
                return 0
            if msg[0] == "[END]":
                break
            else:
                self.username_a.append(msg[0])
                self.user_color_a.append(msg[1])
                try:
                    server.sendall(self.enc("[OK]"))
                except SocketError as e:
                    #print(e)
                    self.popup("Cannot contact server, retry.")
                    return
        try:
            server.sendall(self.enc("[OK]"))
            self.color = self.dec(server.recv(SIZE))
            server.sendall(self.enc("[OK]"))
        except SocketError as e:
            # print(e)
            self.popup("Cannot contact server, retry.")
            return
        layout_recv = [[sg.Multiline(size=(67, 20), font=font1, disabled=True, key="TextBox"),
                        sg.Multiline(size=(17, 20), font=font1, disabled=True, key="ListBox")]]
        layout_send = [
            [sg.Text('Message', font=font2),
             sg.InputText('Message', do_not_clear=False, font=font1, key="Message", size=(61, 1)),
             sg.Button("Send", font=font2, bind_return_key=True, size=(10, 1)),
             sg.Button("Quit", font=font2, button_color="orange", size=(10, 1))]]
        self.window_menu.close()
        self.window.close()
        window_send = sg.Window(title=f"FelpaChat - Logged in as {self.username}", font=font2, layout=[[layout_recv, sg.VSeparator(), layout_send]], finalize=True, icon='./image/icon.ico')
        window_send.TKroot.focus_force()
        receive_t = threading.Thread(target=self.receive_msg, args=(server, window_send,), daemon=True)
        receive_t.start()
        while True:
            event, values = window_send.read()
            if event == "Quit" or event == sg.WINDOW_CLOSED:
                self.quit = True
                try:
                    server.sendall(self.enc("[QUIT]"))
                    server.close()
                    window_send.close()
                    break
                except SocketError as e:
                    #print(e)
                    #self.popup("Cannot contact server, retry.")
                    window_send.close()
                    return 0
            else:
                msg = values["Message"]
                if "[SEP]" in msg:
                    #window_send["TextBox"].print("Cannot send message with keyword '[SEP]'.")
                    self.popup("Cannot send message with keyword '[SEP]'.")
                elif len(msg) > 300:
                    self.popup("Maximun message length is 300 character.")
                elif len(msg) != 0:
                    try:
                        server.sendall(self.enc(msg))
                    except SocketError as e:
                        print(e)
                        #self.popup("Cannot contact server, retry.")
                        window_send.close()
                        return
