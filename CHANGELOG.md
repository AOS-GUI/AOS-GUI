### camel and camelinstall
[added] `camelInstall` refresh button
[changed] package gathering url from `aos-gui.github.io/cInstall` to `raw.githubusercontent.com` counterpart (due to schools blocking all .io domains... for some reason.)
[changed] `cInstall` repo is now `camel` [NOTE: PLEASE CHANGE ALL URLS THAT DIRECT TO OLD TO NEW ON RELEASE]
[changed] search function now selects all apps that fit the query (not just the last one)

> if you'd like to see camel app changelogs, head on over to [camel](https://github.com/AOS-GUI/camel)

### desktop
[added] button icons! (along with setting to turn them on or off)

### editor
[added] editor now has a syntax highlighting toggle
[added] when opening a python file, editor now has a development menu tab where you can run your apps
[added] asks if you'd like to save when opening a new file
[added] new window menu option
[added] dynamic syntax highlighting
[added] menu option to swap between tabs and spaces
[changed] default font is now consolas because i woke up and realized courier new sucks :P
[fixed] occasional character decoding errors
[fixed] some editor quirks
[fixed] markdown syntax highlighting
[fixed] `Run...` menu option in developer mode

### terminal
[added] `cd`, `alias`, `color`, `note`, `edit` commands to terminal
[added] `camel` command multiple package (un)installation
[added] `camel` package upgrading (local ver to server ver if outdated)
[added] environment variables (ex. `%DIR`)
[added] more color feedback!!
[added] slashes to end of dir names when executing `dir`
[added] `-n | --nolinenum` to `read`
[added] you can now type a regular pipe (|) or grave (\`) character by doubling it (eg. || or \`\`)
[fixed] command return inconsistencies
[removed] "enter" button (who used that thing anyway?)

### settings
[added] menu bar item refresh rate option
[added] per-cpu usage percentage menu bar item
[added] live theme preview
[added] show qsplash option
[fixed] issue where occasionally all menu bar items would duplicate
[fixed] for some reason the `show splash` values were swapped (true = don't show & vice versa) (what was i on??)

### updater
[added] updater app, alerts you if your current AOS installation is outdated
> note: only prompts you if it's in autorun.aos!

### splash window
[removed] useless config file write if checkbox is not ticked
[removed] useless `splashes` and `version` reads

### documentation
[added] `top` hyperlink to go to top, and bottom `back` link
[fixed] design and grammar

### splashes
[added] more splashes
[removed] cringe splash texts

### menu bar
[added] extra `|` spacer between edge and AOS-GUI menu

### sdk
[added] `Camel()` class to SDK
[added] `getSplashText()`
[changed] instead of displaying a message box, `openApplication()` simply returns int, and maybe error

### misc
[added] AOS SDK import and QPalette applier to `template.py`
[added] startup sound now plays parallel to the main application!
[added] welcome.txt on new install :)
[changed] `MDs` folder to `docs`
[removed] unused .rndr code
[fixed] autorun apps running before password was entered
[fixed] message box colors not being set to the current theme