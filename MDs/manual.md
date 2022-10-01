# AOS-GUI user manual

Welcome to the USER MANUAL!

## UI

### AOS-GUI differences between host OSs

### Windows

AOS-GUI was designed on Windows, so it looks the best there. All features listed in every update are fully supported on Windows.

### Mac OS
On Mac OS, the menubar is only available when you move the mouse to the top of the screen, and many but not all features will be supported on Mac OS. Mac OS will have better support in later versions.

### Linux
I have not yet tested AOS-GUI on Linux. Please let me know if you own a Linux machine and would be willing to test AOS-GUI on it!

### the menubar

The menubar is located at the top of your screen.

Contained within it is the main menu, which you can access by clicking on `AOS - (username)`. Inside of this menu are the actions `Run...`, `Settings`, `Restart`, and `Exit`. It also contains the clock.

### menubar actions

| Action | Description|
|------|------------|
|Run...|Run a program. This can be a system or a custom app (custom apps are recognized in (AOS)/files/apps/|
|Settings|Accesses settings|
|Restart|Restarts AOS|
|Exit|Exits AOS|

### desktop

The desktop is what contains all of the buttons that link to applications. You can customize which buttons are on the desktop in the `settings` app. To customize the locations of each button, simply drag and drop a button to the new location.

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

### aterm / terminal

AOS terminal. Commands are listed in-app by typing `help` and pressing enter.

### calculator

Your standard, run-of-the-mill calculator app. There are built-in keybinds for the number keys and math operation keys (1-9, +,-,*,/, etc.).

### camelInstall

camelInstall is AOS's package manager. It contains information on both your installed packages and online packages that you can install from the camelInstall database.

**-- Tab "installed" --**

Click on an app in the table and select "Uninstall..." to uninstall it from AOS.

**-- Tab "database" --**

The table here can either contain a list of apps or a notification that you don't have internet. If you have internet, then the following actions can be performed after selecting an app.

| Button | Action|
|------|------------|
|Install| Install the app|
|View Source|View the source code of the app|
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