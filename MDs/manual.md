# AOS-GUI user manual

Welcome to the USER MANUAL!

## UI

### menubar

The menubar is located at the top of your screen, as shown below.

(image)

Contained within it is the main menu, which you can access by clicking on `AOS - (username)`. Inside of this menu are the actions `Run...`, `Settings`, and `Exit`.

### menubar actions

| Action | Description|
|------|------------|
|Run...| Run a program. This can be a system or a custom app (custom apps are recognized in `(AOS)/files/apps/`|
|Settings| Accesses settings|
|Exit|Exits AOS|

### desktop

The desktop is what contains all of the buttons that link to applications. You can customize which buttons are on the desktop in the `settings` app.

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

### aterm

AOS terminal. Commands are listed in-app by typing `help` and pressing enter.

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