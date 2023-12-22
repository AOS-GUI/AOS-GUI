<a href="docs/help.md">back</a>

# sdk
AOS SDK documentation

If you would like some shorthand functions for actions in AOS, add the line `from sdk.sdk import *` to the top of the file (if your app is a QWidget, use `files.apps.sdk.sdk` instead).

The SDK's source code is located in `/files/apps/sdk/`.

## standard functions and classes

| Function | Action |
|----------|--------|
| `compareVersion(v1, v2) -> int` | Compares two version numbers as strings. If `v1` is smaller than `v2`, returns -1 and vice versa. 0 is returned if they are the same. |
| `DraggableButton(QPushButton) -> DraggableButton` | Creates a new QPushButton object, but the button is draggable. |
| `getAOSdir() -> str` | Returns the current working AOS directory as `(directory to AOS-GUI folder)/files/`. |
| `getPalette() -> QPalette` | Returns the current QPalette. |
| `getSettings() -> ConfigParser`| Returns a configparser object with the contents of data.aos loaded. |
| `getSplashText(withHTML=False) -> str` | Returns a random splash text from `/system/data/splashes`.|
| `getTheme() -> list, int` | Returns the current theme colors. On success returns 0, -1 otherwise.|
| `getVersion() -> str` | Returns the current AOS version. |
| `msgBox(text, title="AOS-GUI", icon=..., buttons=OK, x=None, y=None) -> int` | Creates a message box. Refer to Qt5 manual to see what each return int stands for. |
| `promptBox(text, title="AOS-GUI", parent=None, x=None, y=None, mode="text", args=None) -> Union[int, str]` | Creates a prompt box. `mode` should be one of four options: `text`, `int`, `double`, or `item`. If `item` is `mode`, then the `args` argument should be set to your list of items. Returns -1 on fail and the input on success. |
| `openApplication(app, path="files/apps/") -> int, Union[None, Exception]` | Opens an external application. By default checks in `/files/apps/` for the app. Returns -1 and the exception on fail and 0 on success.|
| `restart() -> None` | Restarts AOS-GUI. |
| `toBool(str="") -> bool` | converts a string to a boolean. Returns `True` if string is "True", false otherwise.|

## `Camel()` class

The `Camel()` class contains functions that help with managing packages.

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

<a href="docs/help.md">back</a> | <a href="#sdk">top</a>