# Network-Chat-Room
## How 2 download
### Client

If you're using Windows 11 with     `PySide6`, download [ClientFWUI.py](src/ClientFWUI.py)  
If you're using Windows 10- , MacOS or Linux with `tkinter`,or you didn't install `Pyside6` on your computer, download [ClientTk.py](src/ClientFWUI.py)  
If you're using iOS/Android or your python even haven't got a `tkinter`, please download [ClientTUI.py](src/ClientTUI.py)  
What? You said ClientTUI looks not good in your computer? Try [ClientConsole.py](src/ClientConsole.py). It's pure enough.  
#### Which can I download if my computer have no python?
Common Linux and MacOS all have Python.
If you're Windows without Python , I'll upload it later.

### Server
If you're using Windows, MacOS or Linux with `tkinter` on your computer, download [Server.py](src/server.py)  
What? you're using iOS/Android or you got a python without `tkinter`, please download [ServerTUI.py](src/ServerTUI.py)  
If you said the UI looks not good in your computer? Try [ServerConsole.py](src/ServerConsole.py).

### Which can I download if my computer have no python?
Common Linux and MacOS all have Python.
If you're Windows without Python , I'll upload it later.

## How 2 Use
### Client
1. Select the language in the terminal(or the listbox above the title in the window).
2. Enter ur username.
3. Type the IP address and the port of the server(need a running server).
4. If you see yourself entered the chat interface, congratulations, you entered this server.
### Server
1. Select the language in the terminal(or a listbox showed `English` or `中文`)
2. Select the ip.
3. Enter the port.
4. Click the `▶` button to run a server
5. You can also click the `■` button to stop the server.

## Something Else
For Arabic Users, I recommend you not use the TUI or Console ones.Now some terminal have no RTL supportation, some words like `العربية` may show like `ةيبرعلا`.So I removed arabic in TUI and Console version
