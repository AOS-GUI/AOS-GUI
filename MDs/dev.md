<a href="MDs/help.md">back</a>
# app development guide

If you're here, it probably means that you want to make an app for AOS-GUI!

## get started

1. Grab `template.py` from /MDs/resources/
2. Open it in your favorite IDE / text editor

## making your app

### adding metadata

First, take a look at the comment on line 8:

`#~template|template project|v0.1`

AOS pulls the name, description, and version of your app from this comment in programs such as `camelInstall`. For users to recognize your app, replace the template values with whatever you like. 

    note: the "name" section must be the same as your python module name.

Metadata comment format:
`#~(NAME)|(DESCRIPTION)|(VERSION)`

### making the app work

Replace every string that contains "template" with your own values. Then, simply type in your PyQt5 code as you would in an application of your own.

    note: this template uses "QWidget", but "QMainWindow" works as well.

For example, here is `template.py`:

```python
class template(QWidget):
    def __init__(self):
        super(template, self).__init__()
        self.setFixedSize(500, 500) # does not have to be fixed size
        self.setWindowTitle("template!")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

window = template()
window.show()
```
And here is what a modified version may look like:
```python
class userapp(QWidget):
    def __init__(self):
        super(userapp, self).__init__()
        self.setFixedSize(500, 500) # does not have to be fixed size
        self.setWindowTitle("My awesome application!")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

# more functions / code may go here

window = userapp()
window.show()
```

## sdk

If you would like some shorthand functions for actions in AOS, add the line `from sdk.sdk import *` to the top of the file (if your app is a QWidget, use `files.apps.sdk.sdk` instead). All functions within this "SDK" are documented below.

| Function | Action |
|----------|--------|
| `aosVersion() -> str` | Returns the current AOS version. |
| `DraggableButton(QPushButton) -> DraggableButton object` | Creates a new QPushButton object, but the button is draggable. |
| `getAOSdir() -> str` | Returns the current working AOS directory. |
| `getPalette() -> QPalette` | Returns the current QPalette. |
| `msgBox(text, title="AOS-GUI", icon=..., buttons=OK, x=None, y=None) -> int` | Creates a message box. Refer to Qt5 manual to see what each return int stands for. |
| `openApplication(app, path="files/apps/", silentFail=False) -> int` | Opens an external application. By default checks in files/apps/ for the app. If silentFail is true, no messagebox will appear on fail. Returns -1 on fail and 1 on success.|
| `toBool(str="") -> bool` | converts a string to a boolean. Returns `True` if string is "True", false otherwise|
| `userSettings() -> list`| Returns contents of `data.aos` (data.aos splitted by newlines) |
| `userTheme() -> list` | Returns the current theme colors.|

## publishing your app

To publish your app, create a pull request at [camelInstall](https://github.com/nanobot567/cInstall) with the following contents:

- your change to appList.txt located in `/dl/`
- your python module in `/dl/` if you would like to store it in the database

Your change to appList.txt should ONLY contain your python module name, description, version number, and URL to the module. The URL portion can be a direct link to your python module, or it can be `dl/` followed by the module name if the module is in the camelInstall GitHub repository.

If your app requires assets that cannot be provided in a standalone module, you can specify the URLs of extra assets using a semicolon (`;`). You may also store these assets in the database, but they must be within a folder named `/assets/(moduleName)/`. Everything requested for download within the `/assets/` folder will be installed to the `apps/assets/(appname)/` folder in AOS. A shorthand for your app's asset directory is `assets/`.

Example: (`Test|testing|1.0|/dl/test.py;assets/functions.py`).

When adding extra assets, any path towards any file must be a direct path to the file, starting from the /AOS-GUI/ directory. For example, /assets/myapp/image.png becomes /files/apps/assets/myapp/image.png.

The format of each line in appList.txt is `(NAME)|(DESCRIPTION)|(VERSION)|(URL)`.