import socket
import threading
import random
from socket import error as SocketError
import PySimpleGUI as sg
import playsound

font1=("Helvetica", 14)
font2=("Helvetica", 12)


class felpa_server():
    def __init__(self, host, port, dimension, username, password_hash, password_b64, window_menu):
        self.host = host
        self.port = port
        self.dimension = dimension
        self.username = username
        self.username_a = [username]
        self.conn_clients = []
        self.password_hash = password_hash
        self.password_b64 = password_b64
        self.window_menu = window_menu
        self.color = ['lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
                  'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
                  'light slate gray', 'gray', 'light gray', 'midnight blue', 'navy', 'cornflower blue',
                  'dark slate blue',
                  'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
                  'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
                  'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
                  'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green',
                  'dark olive green',
                  'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
                  'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
                  'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
                  'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
                  'indian red', 'saddle brown', 'sandy brown',
                  'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
                  'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
                  'pale violet red', 'maroon', 'medium violet red', 'violet red',
                  'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
                  'thistle', 'snow2', 'snow3',
                  'snow4', 'seashell2', 'seashell3', 'seashell4',
                  'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
                  'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
                  'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
                  'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
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
                  'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
                  'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
                  'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
                  'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
                  'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
                  'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
                  'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
                  'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
                  'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
                  'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
                  'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
                  'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
                  'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
                  'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
                  'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
                  'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
                  'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
                  'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
                  'grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10',
                  'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19',
                  'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28',
                  'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37',
                  'grey38', 'grey39', 'grey40', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47',
                  'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56',
                  'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65',
                  'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74',
                  'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83',
                  'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92',
                  'grey93', 'grey94', 'grey95', 'grey97', 'grey98', 'grey99']

    def admin_command(self, command):
        if command.startswith("help"):
            return "/kick <Username>    --->    kick user from FelpaChat."
        elif command.startswith("kick"):
            cmd = command.split(" ")
            if len(cmd) != 2:
                return "Invalid use of command /kick <Username>."
            elif cmd[1] in self.username_a and cmd[1] != "Admin":
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
        else:
            return "Invalid command."

    def broadcast(self, msg):
        for x in self.conn_clients:
            x.sendall(msg.encode())

    def update(self, s, window_send):
        while (True):
            try:
                conn, addr = s.accept()
                if self.dimension == 0:
                    conn.sendall("[FULL]".encode())
                else:
                    conn.sendall("[OK]".encode())
                    self.dimension -= 1
                    connection_t = threading.Thread(target=self.connection_loop, args=(conn, window_send,), daemon=True)
                    connection_t.start()
            except SocketError as e:
                #print(e)
                break

    def connection_loop(self, conn, window_send):
        try:
            username = ""
            color = ""
            with conn:
                password = conn.recv(1024).decode()
                if password != self.password_hash:  # Step 1 check if password is correct
                    conn.sendall("[DENIED]".encode())
                    #self.conn_clients.remove(conn)
                    return
                else:
                    conn.sendall("[GRANTED]".encode())
                username = conn.recv(1024).decode()  # Step 2 set the username
                if username in self.username_a:
                    #self.conn_clients.remove(conn)
                    return
                else:
                    conn.sendall("[OK_NAME]".encode())

                self.conn_clients.append(conn)
                self.username_a.append(username)

                rnd = random.randint(0, len(self.color)-1)
                color = self.color[rnd]
                self.color.remove(color)
                conn.sendall(f"{color}".encode())  # Step 3 send the color assigned for the user

                conn.recv(1024).decode()

                window_send["TextBox"].print(f"[+] {username} connected to FelpaChat!", background_color='SeaGreen1', end='')
                window_send["TextBox"].print('\n', end='')
                self.broadcast(f"[+] {username} joined FelpaChat!")
                playsound.playsound("incoming.wav")

                while True:
                    client_msg = conn.recv(1024).decode()
                    if client_msg == "[QUIT]":
                        client_msg = f"{username} disconnected from FelpaChat."
                        self.broadcast(f"[-] {client_msg}")
                        self.conn_clients.remove(conn)
                        self.username_a.remove(username)
                        self.color.append(color)
                        self.dimension += 1
                        window_send["TextBox"].print(f"[+] {username} disconnected to FelpaChat!", background_color='Orange', end='')
                        window_send["TextBox"].print('\n', end='')
                        playsound.playsound("error.wav", False)
                        break
                    else:
                        window_send["TextBox"].print(username, text_color=color, end='')
                        window_send["TextBox"].print(": " + client_msg)
                        self.broadcast(f"{username}[SEP]{color}[SEP]{client_msg}")
                        playsound.playsound("incoming.wav")
        except SocketError as e:
            #print(e)
            self.conn_clients.remove(conn)
            self.username_a.remove(username)
            self.color.append(color)
            self.dimension += 1
            window_send["TextBox"].print(f"[+] {username} disconnected to FelpaChat!", background_color='Orange', end='')
            window_send["TextBox"].print('\n', end='')
            client_msg = f"{username} disconnected from FelpaChat."
            self.broadcast(f"[-] {client_msg}")
            playsound.playsound("incoming.wav")

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

            layout_recv = [[sg.Multiline(size=(67, 20), font=font1, disabled=True, key="TextBox")]]
            layout_send = [
                [sg.Text('Message', font=font2), sg.InputText('Message', do_not_clear=False, font=font1, key="Message"),
                 sg.Button("Send", font=font2, button_color="green", bind_return_key=True, size=(8,1)),
                 sg.Button("Quit", font=font2, button_color="orange", size=(8,1))]]
            window_send = sg.Window(title=f"FelpaChat - Server", font=font2, layout=[[layout_recv, sg.VSeparator(), layout_send]], finalize=True)

            update_t = threading.Thread(target=self.update, args=(s, window_send,), daemon=True)
            update_t.start()

            window_send.TKroot.focus_force()

            window_send["TextBox"].print(f"[+] Server started on port {self.port}, waiting for connections.", background_color='SeaGreen1', end='')
            window_send["TextBox"].print('\n', end='')
            playsound.playsound("connected.wav", False)
            while (True):
                try:
                    event, values = window_send.read()
                    if event == "Quit" or event == sg.WINDOW_CLOSED:
                        s.close()
                        window_send.close()
                        break
                    msg = values["Message"]
                    if msg.startswith("/"):
                        cmd_res = self.admin_command(msg[1:])
                        window_send["TextBox"].print(cmd_res)
                    else:
                        window_send["TextBox"].print(f"[{self.username}] ", text_color="red", end='')
                        window_send["TextBox"].print(": " + msg)
                        self.broadcast(f"Admin[SEP]red[SEP]{msg}")
                except Exception as e:
                    #print(e)
                    break
