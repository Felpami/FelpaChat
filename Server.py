import socket
import threading
import random
import PySimpleGUI as sg
import playsound
import base64
import time
from socket import error as SocketError
from Crypto.Cipher import AES

font1=("Helvetica", 14)
font2=("Helvetica", 12)
SIZE = 512


class felpa_server():
    def __init__(self, host, port, dimension, username, password_hash, window_menu):
        self.host = host
        self.port = port
        self.dimension = dimension
        self.username = username
        self.username_a = [f"[{username}]"]
        self.user_color_a = ["red"]
        self.conn_clients = []
        self.password_hash = password_hash
        self.window_menu = window_menu
        self.quit = False
        self.color = ['lemon chiffon', 'azure', 'alice blue', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
                  'light slate gray', 'gray', 'midnight blue', 'navy', 'cornflower blue',
                  'dark slate blue',
                  'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
                  'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
                  'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
                  'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green',
                  'dark olive green',
                  'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
                  'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
                  'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
                  'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
                  'saddle brown', 'sandy brown',
                  'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
                  'coral', 'light coral', 'tomato', 'orange red', 'hot pink', 'deep pink', 'pink', 'light pink',
                  'maroon', 'medium violet red',
                  'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
                  'thistle', 'snow4', 'seashell2', 'seashell3', 'seashell4',
                  'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
                  'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
                  'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
                  'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
                  'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
                  'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
                  'LightSkyBlue3', 'LightSkyBlue4', 'Slategray1', 'Slategray2', 'Slategray3',
                  'Slategray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
                  'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
                  'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
                  'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
                  'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
                  'cyan4', 'DarkSlategray1', 'DarkSlategray2', 'DarkSlategray3', 'DarkSlategray4',
                  'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
                  'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
                  'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
                  'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
                  'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
                  'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
                  'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
                  'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
                  'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
                  'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
                  'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'sienna1', 'sienna2', 'sienna3', 'sienna4',
                  'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4',
                  'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
                  'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
                  'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
                  'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
                  'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4','DeepPink2', 'DeepPink3',
                  'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
                  'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4',
                  'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
                  'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
                  'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
                  'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
                  'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
                  'grey1', 'grey2', 'grey3', 'grey4', 'grey5']


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
            return False

    def user_list_update(self, window_send):
        window_send["ListBox"].update("")
        i = 0
        for user in self.username_a:
            # window_send["ListBox"].print(user, text_color=self.user_color_a[self.username_a.index(user)])
            window_send["ListBox"].print(user, text_color=self.user_color_a[i])
            i += 1

    def admin_command(self, command):
        if command.startswith("help"):
            return "/kick <Username>    --->    Kick user from FelpaChat.\n/log                            --->    Start to log chat to a file."
        elif command.startswith("kick"):
            cmd = command.split(" ")
            if len(cmd) != 2:
                return "Invalid use of command /kick <Username>."
            elif cmd[1] in self.username_a and cmd[1] != self.username:
                position = self.username_a.index(cmd[1])
                try:
                    self.conn_clients[position-1].close()
                    return f"[+] {cmd[1]} kicked successfully!"
                except (SocketError, Exception) as e:
                    #print(e)
                    return "Error."
                    pass
            else:
                return "Clients do not exists."
        elif command.startswith("log"):
            return "Started logging to C:\\HEHE"
        else:
            return "Invalid command."

    def broadcast(self, msg, conn_array):
        for x in conn_array:
            try:
                x.sendall(self.enc(msg))
            except SocketError as e:
                print(e)
                pass

    def update(self, s, window_send):
        while (True):
            try:
                conn, addr = s.accept()
            except SocketError as e:
                print(e)
                break
            if self.dimension == 0:
                try:
                    with conn:
                        conn.sendall(self.enc("[SERVER_FULL]"))
                except SocketError as e:
                    print(e)
                    break
            else:
                try:
                    conn.sendall(self.enc("[SERVER_OK]"))
                except SocketError as e:
                    print(e)
                    break
                connection_t = threading.Thread(target=self.connection_loop, args=(conn, window_send,), daemon=True)
                connection_t.start()

    def connection_loop(self, conn, window_send):
        color = ""
        username = ""
        try:
            conn.settimeout(3)
            username = self.dec(conn.recv(SIZE))
            if username:
                if username in self.username_a:
                    conn.sendall(self.enc("[ERROR_NAME]"))
                    conn.close()
                    return
            else:
                conn.close()
                return
            conn.sendall(self.enc("[OK_NAME]"))
            self.conn_clients.append(conn)
            self.username_a.append(username)
            i = 0
            for user in self.username_a[:-1]:
                conn.sendall(self.enc(f"{user}[SEP]{self.user_color_a[i]}"))
                conn.recv(SIZE)
                i += 1
            conn.sendall(self.enc("[END]"))
            conn.recv(SIZE)
            rnd = random.randint(0, len(self.color) - 1)
            color = self.color[rnd]
            self.user_color_a.append(color)
            self.color.remove(color)
            conn.sendall(self.enc(f"{color}"))

            conn.recv(SIZE)
        except SocketError as e:
            print(e)
            conn.close()
            self.conn_clients.remove(conn)
            self.username_a.remove(username)
            self.user_color_a.remove(color)
            self.color.append(color)
            self.dimension += 1
            window_send["TextBox"].print(f"{username} disconnected from FelpaChat[SEP]{color}", text_color='Orange')
            self.user_list_update(window_send)
            index = self.conn_clients.index(conn)
            self.broadcast(f"{username} disconnected from FelpaChat", self.conn_clients[:index] + self.conn_clients[index + 1:])
            playsound.playsound("error.wav", False)
            return
        self.dimension -= 1
        window_send["TextBox"].print(f"{username} connected to FelpaChat", text_color="green")
        #window_send["TextBox"].print('\n', end='')
        self.user_list_update(window_send)
        index = self.conn_clients.index(conn)
        self.broadcast(f"{username} connected to FelpaChat[SEP]{color}", self.conn_clients[:index] + self.conn_clients[index + 1:])
        playsound.playsound("incoming.wav", False)
        conn.settimeout(None)
        while True:
            try:
                client_msg = self.dec(conn.recv(SIZE))
            except SocketError as e:
                #print(e)
                conn.close()
                self.conn_clients.remove(conn)
                self.username_a.remove(username)
                self.user_color_a.remove(color)
                self.color.append(color)
                self.dimension += 1
                window_send["TextBox"].print(f"{username} disconnected from FelpaChat[SEP]{color}", text_color='Orange')
                self.user_list_update(window_send)
                index = self.conn_clients.index(conn)
                self.broadcast(f"{username} disconnected from FelpaChat", self.conn_clients[:index] + self.conn_clients[index + 1:])
                playsound.playsound("error.wav", False)
                break
            if client_msg != "[QUIT]":
                index = self.conn_clients.index(conn)
                self.broadcast(f"{username}[SEP]{color}[SEP]{client_msg}",
                               self.conn_clients[:index] + self.conn_clients[index + 1:])
                window_send["TextBox"].print(username, text_color=color, end='')
                window_send["TextBox"].print(": " + client_msg)
                playsound.playsound("incoming.wav", False)
            else:
                self.conn_clients.remove(conn)
                self.username_a.remove(username)
                self.user_color_a.remove(color)
                self.color.append(color)
                self.dimension += 1
                index = self.conn_clients.index(conn)
                self.broadcast(f"{username} disconnected from FelpaChat[SEP]{color}", self.conn_clients[:index] + self.conn_clients[index + 1:])
                window_send["TextBox"].print(f"{username} disconnected to FelpaChat", text_color='Orange')
                self.user_list_update(window_send)
                playsound.playsound("error.wav", False)
                conn.close()
                break

    def server(self):  # main shell function
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen()
            except SocketError as e:
                #print(str(e))
                return 0
            self.window_menu.close()
            layout_recv = [[sg.Multiline(size=(67, 20), font=font1, disabled=True, key="TextBox"),sg.Multiline(size=(17,20), font=font1, disabled=True, key="ListBox")]]
            layout_send = [
                [sg.Text('Message', font=font2), sg.InputText('Message', do_not_clear=False, font=font1, key="Message",size=(61,1)),
                 sg.Button("Send", font=font2, bind_return_key=True, size=(10,1)),
                 sg.Button("Quit", font=font2, button_color="orange", size=(10,1))]]
            window_send = sg.Window(title=f"FelpaChat - Server", font=font2, layout=[[layout_recv, sg.VSeparator(), layout_send]], finalize=True, icon='./image/icon.ico')
            update_t = threading.Thread(target=self.update, args=(s, window_send,), daemon=True)
            update_t.start()
            window_send.TKroot.focus_force()
            window_send["TextBox"].print(f"Server started on port {self.port}, waiting for connections", text_color='blue')
            window_send["ListBox"].print(f"[{self.username}] ", text_color="red")
            playsound.playsound("connected.wav", False)
            count = 0
            while (True):
                start_timer = time.time()
                event, values = window_send.read()
                ent_timer = time.time()
                count -= max(0, int(ent_timer - start_timer) * 2)
                count = max(0, count)
                if event == "Quit" or event == sg.WINDOW_CLOSED:
                    self.quit = True
                    try:
                        for connection in self.conn_clients:
                            connection.close()
                        s.close()
                        window_send.close()
                        break
                    except SocketError as e:
                        #print(e)
                        window_send.close()
                        break
                msg = values["Message"]
                if msg.startswith("/"):
                    cmd_res = self.admin_command(msg[1:])
                    if cmd_res != "":
                        window_send["TextBox"].print(cmd_res)
                else:
                    if "[SEP]" in msg:
                        #window_send["TextBox"].print("Cannot send message with keyword '[SEP]'.")
                        self.popup("Cannot send message with keyword '[SEP]'.")
                    elif len(msg) > 300:
                        self.popup("Maximun message length is 300 character.")
                    elif len(msg) != 0:
                        if count < 10:
                            window_send["TextBox"].print(f"[{self.username}]", text_color="red", end='')
                            window_send["TextBox"].print(": " + msg)
                            self.broadcast(f"[{self.username}][SEP]red[SEP]{msg}", self.conn_clients)
                            count += 1
                        else:
                            self.popup("Too many message sent.")
