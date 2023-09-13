<a href="docs/help.md">back</a>
# app development guide

If you're here, it probably means that you want to make an app for AOS-GUI!

## get started

1. Grab `template.py` from /docs/resources/
2. Open it in your favorite IDE / text editor

## making your app

### adding metadata

First, take a look at the comment on line 8:

`#~template|template project|v0.1`

AOS pulls the name, description, and version of your app from this comment in programs such as `camelInstall`. For users to recognize your app, replace the template values with whatever you like. 

> note: the "name" section must be the same as your python module name.

Metadata comment format:
`#~(NAME)|(DESCRIPTION)|(VERSION)`

### making the app work

Replace every string that contains "template" with your own values. Then, simply type in your PyQt5 code as you would in an application of your own.

> note: this template uses "QWidget", but "QMainWindow" works as well.

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
| `compareVersion(v1, v2) -> int` | Compares two version numbers. If `v1` is smaller than `v2`, returns -1 and vice versa. 0 is returned if they are the same. |
| `DraggableButton(QPushButton) -> DraggableButton` | Creates a new QPushButton object, but the button is draggable. |
| `getAOSdir() -> str` | Returns the current working AOS directory. |
| `getPalette() -> QPalette` | Returns the current QPalette. |
| `getSettings() -> ConfigParser`| Returns a configparser object with the contents of data.aos loaded. |
| `getSplashText(withHTML=False) -> str` | Returns a random splash text from `/system/data/splashes`.|
| `getTheme() -> list, int` | Returns the current theme colors. On success returns 0, -1 otherwise.|
| `getVersion() -> str` | Returns the current AOS version. |
| `msgBox(text, title="AOS-GUI", icon=..., buttons=OK, x=None, y=None) -> int` | Creates a message box. Refer to Qt5 manual to see what each return int stands for. |
| `promptBox(text, title="AOS-GUI", parent=None, x=None, y=None, mode="text", args=None) -> Union[int, str]` | Creates a prompt box. `mode` should be one of four options: `text`, `int`, `double`, or `item`. If `item` is `mode`, then the `args` argument should be set to your list of items. Returns -1 on fail and the input on success. |
| `openApplication(app, path="files/apps/") -> int, Union[None, Exception]` | Opens an external application. By default checks in files/apps/ for the app. Returns -1 and the exception on fail and 0 on success.|
| `restart() -> None` | Restarts AOS-GUI. |
| `toBool(str="") -> bool` | converts a string to a boolean. Returns `True` if string is "True", false otherwise.|


### `Camel()` class

The `Camel` class contains functions that help with managing packages.

> NOTE: please call `update()` after instantiating the class, as the package list is not gathered automatically.

| Function | Action |
|----------|--------|
|`update() -> int, Union[list, str]`| Updates the stored package list. Returns 0 on success with a list containing the gathered app names, descriptions, versions, and URLs. Returns -1 on fail with a string containing the error message.|
|`install(package) -> int, Union[None, str]`| Installs the specified package. Returns 0 on success, -1 with error message on fail.|
|`uninstall(package) -> int, Union[None, str]`| Uninstalls the specified package. Returns 0 on success, -1 with error message on fail.|
|`getNames() -> list`| Returns the list of package names.|
|`getDescs() -> list`| Returns the list of package descriptions.|
|`getVersions() -> list`| Returns the list of package versions.|
|`getURLs() -> list`| Returns the list of package URLs.|
|`getAppInfo() -> list, list, list, list`| Convenience function. Returns package names, descriptions, versions, and URLs in that order.|
|`isUpdated() -> bool`| Returns `True` if the package list has been updated, false otherwise.|

> if you need help with the `Camel()` class, feel free to look at `/system/cinstall.py`!

## storing user data
If you would like to store user data in your app, the recommended directory is `/apps/assets/(APPNAME)`, but you can store it anywhere you like.

## publishing your app

To publish your app, create a pull request at [camel](https://github.com/nanobot567/camel) with the following contents:

- your change to appList.txt located in `/dl/`
- your python module in `/dl/` if you would like to store it in the database

Your change to `appList.txt` should ONLY contain your python module name, description, version number, and URL to the module. The URL portion can be a direct link to your python module, or it can be `dl/` followed by the module name if the module is in the camelInstall GitHub repository.

If your app requires assets that cannot be provided in a standalone module, you can specify the URLs of extra assets using a semicolon (`;`). You may also store these assets in the database, but they must be within a folder named `/assets/(moduleName)/`. Everything requested for download within the `/assets/` folder will be installed to the `apps/assets/(appname)/` folder in AOS. A shorthand for your app's asset directory is `assets/`.

Example: (`Test|testing|1.0|/dl/test.py;assets/functions.py`).

When adding extra assets, any path towards any file must be a direct path to the file, starting from the `AOS-GUI/` directory. For example, `/assets/myapp/image.png` becomes `/files/apps/assets/myapp/image.png`.

The format of each line in appList.txt is `(NAME)|(DESCRIPTION)|(VERSION)|(URL)`.

<a href="docs/help.md">back</a> | <a href="#app-development-guide">top</a>