<a href="MDs/help.md">back</a>
# AOS-GUI user manual

Welcome to the USER MANUAL!

## UI

### AOS-GUI differences between host OSs

### Windows

AOS-GUI was designed on Windows, so it looks the best there. All features listed in every update are fully supported on Windows.

### Mac OS
On Mac OS, the menubar is only available when you move the mouse to the top of the screen, and many but not all features will be supported on Mac OS. Mac OS will have better support in later versions.

### Linux
AOS-GUI functions correctly on Linux, and fully supports AOS.

### the menubar

The menubar is located at the top of your screen.

Contained within it is the main menu, which you can access by clicking on `AOS - (username)`. Inside of this menu are the actions `Run...`, `Settings`, `Restart`, and `Exit`. Alongside this is the extras menu, and the menubar widgets that you have chosen to add to the menubar in settings (clock, cpu usage, etc.).

### menubar actions

| Action | Description|
|------|------------|
|Run...|Run a program. This can be a system or a custom app (custom apps are recognized in (AOS)/files/apps/|
|Settings|Accesses settings|
|Restart|Restarts AOS|
|Exit|Exits AOS|

### desktop

The desktop is what contains all of the buttons that link to applications. You can customize which buttons are on the desktop in the `settings` app. To customize the locations of each button, simply drag and drop a button to the new location.

If you would like to create a shortcut to an external app, click on the `Extras` menu in the menu bar and click `Create Shortcut...`, then type the name of the app you would like to add to the desktop and press OK. To remove this shortcut, click on `Remove Shortcut...`, type the text displayed on the button you would like to remove, and click OK.

While focusing on the desktop, shortcuts that you have bound in `settings` can be called by pressing the key combos you have set. The default keybinds are:

| Action | Key Combo|
|------|------------|
|Run...|Ctrl+R|
|Terminal|Ctrl+T|
|Settings|Ctrl+Shift+S|
|Help|Ctrl+H|

## apps

Documentation on all of the AOS-GUI system apps is below.

### AOShelp

Displays help on AOS-GUI. Note that the help text is taken straight from a markdown file and has not been modified to look better in AOS.

### appLauncher

This app launches external apps that you have downloaded via camelInstall.

| Button | Action|
|------|------------|
|Launch App| Run the selected app|
|Refresh|Refresh the app list|

### calculator

Your standard, run-of-the-mill calculator app. There are built-in keybinds for the number keys and math operation keys (1-9, +,-,*,/, etc.).

### camelInstall

camelInstall is AOS's package manager. It contains information on both your installed packages and online packages that you can install from the camelInstall database.

**-- Tab "installed" --**

Click on an app in the table and select "Uninstall..." to uninstall it from AOS. You can also click "Run" to run the selected app.

**-- Tab "database" --**

The table here can either contain a list of apps or a notification that you don't have internet. If you have internet, then the following actions can be performed after selecting an app.

| Button | Action|
|------|------------|
|Install| Install the app|
|Search|Searches the database for any reference of the words typed|

### editor

AOS editor. Here you can edit text files.

| Button | Action|
|------|------------|
|New| Create a new file|
|Open|Opens a file|
|Save|Saves the file|
|Save as...|Saves the file as a new file|

### fs (filesystem)

AOS filesystem viewer. Here you can view all of the folders and files within the AOS `/` directory.

### settings

AOS settings. Here you can change all of AOS's settings (surprising, I know).

### terminal

AOS terminal. Commands are listed in-app by typing `help` and pressing enter.

## other useful information

### `.aos` files
`.aos` files contain data used in AOS frequently. Below is information on how each of these files are formatted.

- `data.aos`
    - each value in `data.aos` is separated by a newline
    - corresponding keys (by line)
        1. username
        2. password
        3. color theme
        4. font size
        5. shortcut to run...
        6. shortcut to terminal
        7. shortcut to settings
        8. shortcut to help
        9. system apps shown on desktop, separated by pipes
        10. show splash screen
        11. gui theme
        12. clock mode (true = 24 hour)
        13. button dimensions
        14. play startup sound
        15. use color theme within apps
- `desktop.aos`
    - stores desktop shortcuts. each shortcut is separated by a pipe.
- `menubar.aos`
    - stores each item in the menubar. each item is separated by a pipe.
- `autorun.aos`
    - stores apps to be executed on startup. each item is separated by a pipe.

### `.theme` files
`.theme` files contain information about color themes in AOS. every value is separated by a newline.

corresponding keys (by line)
1. text color
2. desktop background color
3. taskbar text color
4. taskbar background color
5. button text color
6. button background color
7. window background color