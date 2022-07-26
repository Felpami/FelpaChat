from Server import felpa_server
from Client import felpa_client
import PySimpleGUI as sg
import hashlib
import socket

font1=("Helvetica", 14)
font2=("Helvetica", 12)
font3=("Helvetica", 9)


def popup(str):
    layout_popup = [[sg.Text(str)], [sg.Button("Exit", key="Exit", size=(13, 1), button_color="orange")]]
    layout = [[sg.Column(layout_popup,element_justification="c")]]
    window_popup = sg.Window(title="Error", font=font2, layout=layout, finalize=True, icon='./image/icon.ico')
    window_popup.TKroot.focus_force()
    window_popup.read(close=True)

def get_local_ip(): #grab the local ip
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))

        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close()

def main():
    sg.theme("BrownBlue")
    layout_menu = [[sg.Text('             Welcome to FelpaChat!', font=font2)],
                   [sg.Text("----------------------------------------------------", font=font2)],
                   [sg.Text("Felpami - https://github.com/Felpami/FelpaChat", font=font3)],
                   [sg.Button("Connect to a server", font=font2, size=(29, 1), key="Connect")],
                   [sg.Button("Host a server", font=font2, size=(29, 1), key="Host")],
                   [sg.Button("Quit", font=font2, button_color="orange", size=(29, 1), key="Quit")]]
    window_menu = sg.Window(title="FelpaChat Menu", font=font2, layout=layout_menu, finalize=True, icon='./image/icon.ico')
    window_menu.TKroot.focus_force()
    IP = get_local_ip()
    store_connect = ["", 7777, "", "Password"]
    store_host = [IP, 7777, 5, "Admin", "Password"]
    while True:
        try:
            event, values = window_menu.read()
        except KeyboardInterrupt:
            return
        if event == "Host":
            while True:
                layout_host = [[sg.Text('Server IP      ', font=font2), sg.InputText(font=font1, key="IP", size=(21,1))],
                               [sg.Text('Server Port  ', font=font2), sg.InputText(font=font1, key="Port", size=(21,1))],
                               [sg.Text('Dimension   ', font=font2), sg.InputText(font=font1, key="Dimension", size=(21, 1))],
                               [sg.Text('UserName   ', font=font2), sg.InputText(font=font1, key="Username", size=(21, 1))],
                               [sg.Text('Password    ', font=font2), sg.InputText(font=font1, key="Password_host", size=(21,1), password_char='*')],
                               [sg.Button("Host", font=font2, bind_return_key=True, size=(17, 1)), sg.Exit(font=font2, button_color="orange", size=(17, 1))]]
                window_host = sg.Window(title="HostForm", font=font2, layout=layout_host, finalize=True, icon='./image/icon.ico')
                window_host.TKroot.focus_force()
                window_host["IP"].Update(store_host[0])
                window_host["Port"].Update(store_host[1])
                window_host["Dimension"].Update(store_host[2])
                window_host["Username"].Update(store_host[3])
                window_host["Password_host"].Update(store_host[4])
                try:
                    event, values = window_host.read()
                except KeyboardInterrupt:
                    return
                if event == "Exit" or event == sg.WINDOW_CLOSED:
                    window_host.close()
                    break
                else:
                    store_host[0] = values["IP"]
                    ip_number_a = store_host[0].split(".")
                    store_host[1] = values["Port"]
                    store_host[2] = values["Dimension"]
                    store_host[3] = values["Username"]
                    store_host[4] = values["Password_host"]
                    if not store_host[1].isdigit():
                        popup("Port must be a number.")
                        store_host[1] = 7777
                        window_host.close()
                    elif int(store_host[1]) > 65536:
                        popup("Incorrect port number.")
                        store_host[1] = 7777
                        window_host.close()
                    elif not store_host[2].isdigit():
                        popup("Dimension must be a number.")
                        store_host[2] = "5"
                        window_host.close()
                    elif len(store_host[2]) > 30:
                        popup("Maximun server dimension is 30.")
                        store_host[2] = "5"
                        window_host.close()
                    elif len(store_host[3]) == 0:
                        popup("username cannot be empty.")
                        window_host.close()
                    elif len(store_host[3]) > 15:
                        popup("Maximun username length is 15 characters.")
                        window_host.close()
                    elif "[SEP]" in store_host[3]:
                        popup("Cannot set username with keyword '[SEP]'.")
                        window_host.close()
                    elif store_host[4] == "":
                        popup("Password cannot be empty.")
                        window_host.close()
                    elif len(store_host[4]) > 300:
                        popup("Maximun password length is 300 characters.")
                        store_host[4] = ""
                        window_host.close()
                    elif len(ip_number_a) != 4:
                        popup("Incorrect IP address.")
                        store_host[0] = IP
                        window_host.close()
                    elif len(ip_number_a) == 4:
                        found = False
                        for number in ip_number_a:
                            if not number.isdigit():
                                popup("Incorrect IP address.")
                                store_host[0] = IP
                                window_host.close()
                                found = True
                                break
                        if not found:
                            password_hash = hashlib.sha256(values["Password_host"].encode()).digest()
                            serv = felpa_server(store_host[0], int(store_host[1]), int(store_host[2]), store_host[3], password_hash, window_menu)
                            window_host.close()
                            ret = serv.server()
                            if ret == 0:
                                popup(f"Cannot start server on port {int(values['Port'])}")
                                window_host.close()
                                del serv
                            else:
                                quit()
        elif event == "Connect":
            while (True):
                layout_connect = [[sg.Text('Server IP      ', font=font2), sg.InputText(font=font1, key="IP", size=(21, 1))],
                                  [sg.Text('Server Port  ', font=font2), sg.InputText(font=font1, key="Port", size=(21, 1))],
                                  [sg.Text('UserName   ', font=font2), sg.InputText(font=font1, key="Username", size=(21, 1))],
                                  [sg.Text('Password    ', font=font2),
                                   sg.InputText(font=font1, key="Password_connect", size=(21, 1), password_char='*')],
                                  [sg.Button("Connect", font=font2, bind_return_key=True, size=(17, 1)),
                                   sg.Exit(font=font2, button_color="orange", size=(17, 1))]]
                window_connect = sg.Window(title="ConnectForm", font=font2, layout=layout_connect, finalize=True, icon='./image/icon.ico')
                window_connect.TKroot.focus_force()
                window_connect["IP"].Update(store_connect[0])
                window_connect["Port"].Update(store_connect[1])
                window_connect["Username"].Update(store_connect[2])
                window_connect["Password_connect"].Update(store_connect[3])
                try:
                    event, values = window_connect.read()
                except KeyboardInterrupt:
                    return
                if event == "Exit" or event == sg.WINDOW_CLOSED:
                    window_connect.close()
                    break
                else:
                    store_connect[0] = values["IP"]
                    ip_number_a = store_connect[0].split(".")
                    store_connect[1] = values["Port"]
                    store_connect[2] = values["Username"]
                    store_connect[3] = values["Password_connect"]
                    if not store_connect[1].isdigit():
                        popup("Port must be a number.")
                        store_connect[1] = 7777
                        window_connect.close()
                    elif int(store_connect[1]) > 65536:
                        popup("Incorrect port number.")
                        store_connect[1] = 7777
                        window_connect.close()
                    elif store_connect[2] == "":
                        popup("Username cannot be empty.")
                        store_connect[2] = ""
                        window_connect.close()
                    elif len(store_connect[2]) > 15:
                        popup("Maximun username length is 15 characters.")
                        store_connect[2] = ""
                        window_connect.close()
                    elif "[SEP]" in store_connect[2]:
                        popup("Cannot set username with keyword '[SEP]'.")
                        store_connect[2] = ""
                        window_connect.close()
                    elif store_connect[3] == "":
                        popup("Password cannot be empty.")
                    elif len(store_connect[3]) > 300:
                        popup("Maximun password length is 300 characters.")
                        store_connect[3] = ""
                        window_connect.close()
                    elif len(ip_number_a) != 4:
                        popup("Incorrect IP address.")
                        store_connect[0] = ""
                        window_connect.close()
                    elif len(ip_number_a) == 4:
                        found = False
                        for number in ip_number_a:
                            if not number.isdigit():
                                popup("Incorrect IP address.")
                                store_connect[0] = ""
                                window_connect.close()
                                found = True
                                break
                        if not found:
                            password_hash = hashlib.sha256(values["Password_connect"].encode()).digest()
                            cln = felpa_client(store_connect[0], int(store_connect[1]), store_connect[2], password_hash,
                                               window_connect, window_menu)
                            ret = cln.client()
                            if ret == 0:
                                popup("Cannot contact server, retry.")
                                window_connect.close()
                                # print("[-] Access denied.")
                                del cln
                            elif ret == 1:
                                popup("Server is already full.")
                                window_connect.close()
                                del cln
                            elif ret == 2:
                                popup("Incorrect password, retry.")
                                window_connect.close()
                                del cln
                            elif ret == 3:
                                popup("Username already in use.")
                                window_connect.close()
                                del cln
                            else:
                                quit()
            #quit()
        elif event == "Quit" or event == sg.WINDOW_CLOSED:
            window_menu.close()
            break



if __name__ == '__main__':
    main()
