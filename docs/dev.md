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

## aos sdk
AOS-GUI provides some functions and classes to aid with software development in AOS. These are documented [here]("/docs/sdk.md").

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

### app icon

Since AOS-GUI version 0.9 beta, apps can have an icon, which is displayed in the shortcut button if it is on the desktop.

Example of an icon in a shortcut:

<img src="docs/resources/images/icon-example.png"></img>

For apps installed from camelInstall, the app's icon must be located in `/files/apps/assets/(app)/icon.(any)`. This icon can be any size, but the recommended size is 64 x 64.

## known quirks and fixes

### QFileDialogs do not stay on top in Linux

Add the option `QFileDialog.DontUseNativeDialog` when initializing the dialog. For example:

`file,check = QFileDialog.getOpenFileName(None, "Open a file", getAOSdir()+"/", "All Files (*)", options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)`

### Menu bars are not the correct color on Windows

Here was my fix for this:

```python

if os.name == "nt":
    self.menuBar().setStyleSheet("""
        QMenuBar {
            background-color: #fff;
                color: #000;
        }
        QMenuBar::item {
            background-color: #fff;
            color: #000;
        }
        QMenuBar::item::selected {
            background-color: #3399cc;
            color: #fff;
        }
        QMenu {
            background-color: #fff;
            color: #000;
        }
        QMenu::item::selected {
            background-color: #333399;
            color: #999;
        }""")

```

<a href="docs/help.md">back</a> | <a href="#app-development-guide">top</a>