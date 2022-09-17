# Installing AOS-GUI

## you will need...

- The latest version of [Python](https://python.org/downloads/)
- The latest version of [pip](https://pip.pypa.io/en/stable/installation/)
- The latest version of AOS-GUI
- Any terminal emulator (for example, Terminal for Mac OS or Command Prompt for Windows)

- At least 60 MB of space on your hard drive (this is for PyQt5)

## instructions

1. Open your terminal emulator
2. Navigate to the folder where AOS-GUI is located using `cd (folder)`
3. Type `python aos-gui.py` and press enter
4. Wait for AOS-GUI to finish installing required modules
5. When prompted, customize AOS however you like
6. Reboot AOS
7. Enjoy AOS!

# Uninstalling AOS-GUI

## instructions

1. Open AOS and navigate to `Settings -> Reset`
2. Click on `Reset AOS...`
3. Confirm that you actually want to reset AOS
4. Wait until AOS finishes uninstalling
5. Delete the AOS-GUI folder

If you want to completely uninstall AOS-GUI, including modules...

1. Perform steps 1-5
2. Open your terminal emulator
3. Type `python3 -m pip uninstall PyQt5 requests playsound`
4. Congratulations! You've successfully uninstalled AOS!