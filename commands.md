# Commands cheatsheet

## These commands are predefined commands, see _spython_tcp.py_(The payload) for more details.

### cmd

- opens cmd

---

### open [app]

- opens [app], e.g open calc

---

### fullscreen

- Puts active window in full screen

---

### exit_prog

- Closes active window

---

### minimise

- minimises active window

---

#### type [str]

- types str, e.g type hello, NOTE if user types "type hello there", everthing after "hello" is ignored

---

### screenshot

- takes screenshot and sends it to attacker in the way it was configured

---

### enter

- simulates Enter key

---

### left, right

- Pretty self explanatory

---

### tcp_reverse

- Creates a reverse shell, type exit to break out

---

### list

- list directory using dir(Windows only)

---

## Note

- the _tcp_reverse_ command takes attacker input runs them in a shell on on the victim's machine , sends the output and closes the shell. To circumvent this, you may need to chain commands using the _&&_ operator
