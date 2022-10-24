# Spython

![flc_design2022102376629](https://user-images.githubusercontent.com/91953982/197397830-3cdd5836-bb62-43c7-bfbf-74977a856a74.png)


## About ##
This simple python script sends keystrokes and  screenshots of victim's machine back to the attacker.
NOTE: This is one of my first actual  project, I've been coding in python for nearly a year so please don't judge the quality of the code :/
Feedbacks(specially bads ones) are appreciated :)

## Installation guide ##
***Note that after running the *requierements.txt*, it should out of the box. However if you decide to use another variant, e.g spython_http.py, you will have to configure a server and process the incoming requests(from the victim)***

## File Structure ##
- *commands.txt* -> Commands that an attacker can run once connection from victim has been established
- *spython_tcp.py* -> The payload, note that variables such as HOST and MAIN_PORT may or may not be manually changed
- *spython_cli.py* -> This file provides the attacker with a command line interface
- *templates* -> This folder contains templates if user decides to automatically generate payload. No need to use *spython_tcp.py* if payload is automatically generate, a  new file called spython.py will be created in current directoty. You may wish to compile it to exe [here](https://pyinstaller.org/) 
- *extras* -> This folder contains variant of the original payload, i.e *spython_tcp.py*.E.g *spython_http.py* uses HTTP post request to send data back attacker's HTTP server

## How it works ##
![image](https://user-images.githubusercontent.com/91953982/197544894-84fdfb20-2e73-4f5b-b4ca-a24dd663afdf.png)
### Glossary ###
- *MAIN PORT* -> TCP port number used by "main/active connection"
- *"main/active connection"* -> TCP connection that the attacker uses to send commands
- *"key connection"* ->  TCP connection that the attacker uses to receive victim keystrokes and store them in a file
- *K_PORT or KPORT or KEY PORT* -> TCP port number used for *"key connection"*

### Explantion ###
- Here we see the attacker listening on three different TCP ports, notice how are ports are increments of one. This is done so the user only needs to enter one port
- When the payload runs the victim's machine two TCP connections are established to the attacker's machine
- In this case, the first connection is on port 5000, which is called the "active/main connection". The attacker uses this connection to send commands or invoke a reverse shell
- The second connection, to port 5001, is called the "key connection"(no pun intented). This connection is used to  send the victim's keystrokes back the attacker. The first increment from *MAIN PORT*, in this 5000, is used for the "key connection"
- The third one, to port 5002, is only initiated when the attacker uses the "active/main connection" to send the *screenshot* command, see *commands.txt*
- Once the connection is established, the image of the victim's screen is sent to the attacker and stored in a file(which is specified by the user). After the data is sent, the victim closes the connection and the attacker continues listening for inbound connnection on the very same port. Note that the second increment from *MAIN PORT*
