# Spython

![flc_design2022102376629](https://user-images.githubusercontent.com/91953982/197397830-3cdd5836-bb62-43c7-bfbf-74977a856a74.png)

## About

This simple python script sends keystrokes and screenshots of victim's machine back to the attacker.
NOTE: This is one of my first actual project, I've been coding in python for nearly a year so please don't judge the quality of the code :/
Feedbacks(specially bads ones) are appreciated :)

## Installation guide

***Note that after running the *requirements.txt*, it should run out of the box. However if you decide to use another variant, e.g spython_http.py, you will have to configure a server and process the incoming requests(from the victim), , manually modify the payload as needed and change necessary parameters. Nevertheless, the installing is pretty simple, just copy and paste the command/s below, you may wish to run it in a virtual envinronment, see [here](https://docs.python.org/3/library/venv.html)***
    
-    `pip3 install -r requirements.txt`

## File Structure

- _commands.txt_ -> Commands that an attacker can run once connection from victim has been established
- _spython_tcp.py_ -> Source code of payload. Feel free to change it if you wish :)
- _spython_cli.py_ -> This file provides the attacker with a command line interface
- _templates_ -> This folder contains templates if user decides to automatically generate payload. No need to use _spython_tcp.py_ if payload is automatically generate, a new file called _payload.py_ will be created in current directory. Furthermore, a compiled  version of the _payload.py_ is also generated with respect to the user's operating system(e.g exe for windows)
- _extras_ -> This folder contains variant of the original payload, i.e _spython_tcp.py_.E.g _spython_http.py_ uses HTTP post request to send data back attacker's HTTP server

## How it works

![image](https://user-images.githubusercontent.com/91953982/197544894-84fdfb20-2e73-4f5b-b4ca-a24dd663afdf.png)

### Glossary

- _MAIN PORT_ -> TCP port number used by "main/active connection"
- _"main/active connection"_ -> TCP connection that the attacker uses to send commands
- _"key connection"_ -> TCP connection that the attacker uses to receive victim keystrokes and store them in a file
- _K_PORT or KPORT or KEY PORT_ -> TCP port number used for _"key connection"_

### Explanation

- Here we see the attacker listening on three different TCP ports, notice how are ports are increments of one. This is done so the user only needs to enter one port
- When the payload runs on the victim's machine, two TCP connections are established to the attacker's machine
- In this case, the first connection is on port 5000, which is called the "active/main connection". The attacker uses this connection to send predefined commands([see _commands.md_](https://github.com/Theguydev/Spython/blob/main/commands.md)) or invoke a reverse shell
- The second connection, to port 5001, is called the "key connection"(no pun intented). This connection is used to send the victim's keystrokes back the attacker. The first increment from _MAIN PORT_, in this case 5000, is used for the "key connection"
- The third one, to port 5002, is only initiated when the attacker uses the "active/main connection" to send the _screenshot_ command, see [_commands.md_](https://github.com/Theguydev/Spython/blob/main/commands.md)
- Once the connection is established, the image of the victim's screen is sent to the attacker and stored in a file(which is specified by the user). After the data is sent, the victim closes the connection and the attacker continues listening for inbound connnection on the very same port. Note that the second increment from _MAIN PORT_, in this case 5002, is used for the third connection(the dashed line on the diagram). No name for this connection yet

## Drawback ##
- To obtain an exe executable, you will have to be in a windows machine(VM works fine). This applies to Linux and Mac

## Important note
- *spython_cli.py*, the cli has been tested on both windows and linux. However, the program works better on linux and you will have a much better there, so choose wisely
---
## Additional notes

- If user decides to not auto generate the payload, he/she may wish to compile the file to exe [here](https://pyinstaller.org/)
- This small project is proof of concept of a simple yet somewhat powerful spyware
- You may enhance the capability of this project by adding support of SSL or even use some python magic to exfiltrate data throught a reverse SSH tunnel using the [paramiko](https://www.paramiko.org/) module
- If user decides not to automatically generate payload, he/she will have to manually change some variables such as _HOST_ and _PORT_ in _spython_tcp.py_
- Spython is currently in pre-alpha state, more features are coming soon!!
