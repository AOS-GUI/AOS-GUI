# Installing AOS-GUI

<h2 align="center">NOTE: AOS-GUI is currently in open beta! If you decide to install AOS and run across a bug, please leave a bug report in the issues tab above!

<hr>

## you will need...

- The latest version of [Python](https://python.org/downloads/) or [Pypy](https://www.pypy.org/download.html). Pypy is recommended if you are concerned about CPU usage and/or speed.
- The latest version of [pip](https://pip.pypa.io/en/stable/installation/)
- The latest version of AOS-GUI (duh)
- Any terminal emulator (for example, Terminal for Mac OS/Linux or Command Prompt for Windows)
- At least 60 MB of space on your hard drive (this is for PyQt5 and other modules that are required)

## instructions

1. Open your terminal emulator
2. Navigate to the folder where AOS-GUI is located using `cd (folder)`
3. Type `python3 -B aos-gui.py` and press enter (the -B is to disable pycache creation, so if you really want to have pycache directories you can remove the -B).
    - alternatively, you can `chmod` `aos-gui.py` so you can run it like an application.
4. Wait for AOS-GUI to finish installing required modules
5. When prompted, customize AOS however you like
6. Have fun!

# Uninstalling AOS-GUI

## instructions

1. Delete the AOS-GUI folder

If you want to completely uninstall AOS-GUI, including modules...

1. Delete the AOS-GUI folder
2. Open your terminal emulator
3. Type `python3 -m pip uninstall PyQt5 requests playsound psutil`
4. Congratulations! You've successfully uninstalled AOS!