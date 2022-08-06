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

Metadata comment format:
`#~(NAME)|(DESCRIPTION)|(VERSION)`

### making the app work

Replace every string that contains "template" with your own values. Then, simply type in your PyQt5 code as you would in an application of your own.

    note: since the "application" is a QWidget, some functions may not be available.

For example, here is `template.py`:

```python
class template(QWidget):
    def __init__(self):
        super(template, self).__init__()
        self.setFixedSize(500, 500)
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
        self.setFixedSize(500, 500)
        self.setWindowTitle("My awesome application!")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

# more functions / code may go here

window = userapp()
window.show()
```

## publishing your app

Currently, there is no official way to distribute apps. Until there is, you can use GitHub or another VSC site / service to publish it.
