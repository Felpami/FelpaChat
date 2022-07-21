from Server import felpa_server
from Client import felpa_client
import PySimpleGUI as sg
import hashlib
import socket
import playsound

font1=("Helvetica", 14)
font2=("Helvetica", 12)
font3=("Helvetica", 9)

def popup(str):
    layout_popup = [[sg.Text(str)], [sg.Button("Exit", key="Exit", size=(13, 1), button_color="orange")]]
    layout = [[sg.Column(layout_popup,element_justification="c")]]
    window_popup = sg.Window(title="Error", font=font2, layout=layout, finalize=True)
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
    layout_menu = [[sg.Text('             Welcome to FelpaChat!', font=font2)],
                   [sg.Text("----------------------------------------------------", font=font2)],
                   [sg.Text("Felpami - https://github.com/Felpami/FelpaChat", font=font3)],
                   [sg.Button("Connect to a server", font=font2, size=(29, 1), key="Connect")],
                   [sg.Button("Host a server", font=font2, size=(29, 1), key="Host")],
                   [sg.Button("Quit", font=font2, button_color="orange", size=(29, 1), key="Quit")]]
    window_menu = sg.Window(title="FelpaChat Menu", font=font2, layout=layout_menu, finalize=True)
    window_menu.TKroot.focus_force()
    store = ["", 7777, ""]
    while True:
        event, values = window_menu.read()
        if event == "Host":
            layout_host = [[sg.Text('Server IP      ', font=font2), sg.InputText(font=font1, key="IP", size=(21,1))],
                           [sg.Text('Server Port  ', font=font2), sg.InputText(font=font1, key="Port", size=(21,1))],
                           [sg.Text('Password    ', font=font2), sg.InputText(font=font1, key="Password_host", size=(21,1), password_char='*')],
                           [sg.Button("Host", font=font2, bind_return_key=True, button_color="green", size=(17, 1)), sg.Exit(font=font2, button_color="orange", size=(17, 1))]]
            window_host = sg.Window(title="HostForm", font=font2, layout=layout_host, finalize=True)
            window_host.TKroot.focus_force()
            window_host["IP"].Update(get_local_ip())
            window_host["Port"].Update(7777)
            event, values = window_host.read()
            if event == "Exit" or event == sg.WINDOW_CLOSED:
                window_host.close()
            else:
                if values["Password_host"] != "":
                    password_hash = hashlib.sha256(values["Password_host"].encode()).hexdigest()
                else:
                    password_hash = " "
                try:
                    if int(values["Port"]) > 65536:
                        popup("Incorrect settings.")
                        window_host.close()
                    else:
                        serv = felpa_server("192.168.0.102", int(values["Port"]), password_hash, window_menu)
                        window_host.close()
                        ret = serv.server()
                        if ret == 0:
                            popup(f"Cannot start server on port {int(values['Port'])}")
                            window_host.close()
                            del serv
                        quit()
                except Exception as e:
                    #print(e)
                    popup("Incorrect settings.")
                    window_host.close()
        elif event == "Connect":
            while (True):
                layout_connect = [[sg.Text('Server IP      ', font=font2), sg.InputText(font=font1, key="IP", size=(21, 1))],
                                  [sg.Text('Server Port  ', font=font2), sg.InputText(font=font1, key="Port", size=(21, 1))],
                                  [sg.Text('UserName   ', font=font2), sg.InputText(font=font1, key="Username", size=(21, 1))],
                                  [sg.Text('Password    ', font=font2),
                                   sg.InputText(font=font1, key="Password_connect", size=(21, 1), password_char='*')],
                                  [sg.Button("Connect", font=font2, bind_return_key=True, size=(17, 1), button_color="green"),
                                   sg.Exit(font=font2, button_color="orange", size=(17, 1))]]
                window_connect = sg.Window(title="ConnectForm", font=font2, layout=layout_connect, finalize=True)
                window_connect.TKroot.focus_force()
                window_connect["IP"].Update(store[0])
                window_connect["Port"].Update(store[1])
                window_connect["Username"].Update(store[2])
                event, values = window_connect.read()
                if event == "Exit" or event == sg.WINDOW_CLOSED:
                    window_connect.close()
                    break
                else:
                    if values["Password_connect"] != "":
                        password_hash = hashlib.sha256(values["Password_connect"].encode()).hexdigest()
                    else:
                        password_hash = " "

                    try:
                        store[0] = values["IP"]
                        store[1] = int(values["Port"])
                        store[2] = values["Username"]
                        if store[1] > 65536 or store[0] == "" or store[2] == "":
                            popup("Incorrect settings.")
                            window_connect.close()
                        else:
                            cln = felpa_client(store[0], store[1], store[2], password_hash,
                                               window_connect, window_menu)
                            ret = cln.client()
                            if ret == 0:
                                popup("Cannot contact server, retry.")
                                window_connect.close()
                                # print("[-] Access denied.")
                                del cln
                            elif ret == 1:
                                popup("Incorrect password, retry.")
                                window_connect.close()
                            elif ret == 2:
                                popup("Username already in use.")
                                window_connect.close()
                            else:
                                break
                    except Exception as e:
                        #print(e)
                        popup("Incorrect settings.")
                        window_connect.close()
            #quit()
        elif event == "Quit" or event == sg.WINDOW_CLOSED:
            window_menu.close()
            break



if __name__ == '__main__':
    main()
