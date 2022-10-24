# Spython

![flc_design2022102376629](https://user-images.githubusercontent.com/91953982/197397830-3cdd5836-bb62-43c7-bfbf-74977a856a74.png)


## About ##
This simple python script sends keystrokes and  screenshots of victim's machine back to the attacker.
NOTE: This is one of my first actual  project, I've been coding in python for nearly a year so please don't judge the quality of the code :/
Feedbacks(specially bads ones) are appreciated :)

## File Structure ##
- *commands.txt* -> Commands that an attacker can run once connection from victim has been established
- *spython_tcp.py* -> The payload, note that variables such as HOST and MAIN_PORT may or may not be manually changed
- *spython_cli.py* -> This file provides the attacker with a command line interface
- *templates* -> This folder contains templates if user decides to automatically generate payload. No need to use *spython_tcp.py* if payload is automatically generate, a  new file called spython.py will be created in current directoty. You may wish to compile it to exe [here](https://pyinstaller.org/) 
- *extras* -> This folder contains variant of the original payload, i.e *spython_tcp.py*.E.g *spython_http.py* uses HTTP post request to send data back attacker's HTTP server

## How it works ##
