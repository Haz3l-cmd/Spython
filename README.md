# Spython

![flc_design2022102376629](https://user-images.githubusercontent.com/91953982/197397830-3cdd5836-bb62-43c7-bfbf-74977a856a74.png)


This simple python script is able to log keystrokes,take screenshots and send all of that through a POST request to a properly configured HTTP. Moreover, upon running this script, two tcp connections are initiated. One to the attacker's machine on a specififc port which he/she is listening on(e.g using netcat), and the second one to the HTTP server(I used NGINX). The keystrokes and screenshot images are saved to a file on the server. Furthermore these files can be served throught the web browser where the attacker can view them(Maybe serve it through localhost if HTTP server is on the same machine). The other connection is used by the attacker to send predefined command, see commands.txt or even better just look at the source code. Feel free to change the necessary variables such as PORT and HOST. You can compile the source code into exe file [here](https://pyinstaller.org/).
