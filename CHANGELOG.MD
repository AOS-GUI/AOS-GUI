[added] table sorting in camelinstall
[added] `dl` command to terminal (downloads contents of a URL)
[added] wallpaper support, with some default wallpapers located in `/system/data/user/wallpapers/`. supported file formats include BMP, GIF, JPG, PNG, PBM, PGM, PPM, XBM and XPM
[added] `camel` terminal command now supports local package info grabbing, as well as package searching
[changed] AOS editor. changes include QWidget -> QMainWindow, syntax highlighting for python, markdown, and terminal scripts (`.script`,`.aosh`), and word wrap support
[changed] `dir` command in terminal now has a `--notypes` shorthand, `-n`
[changed] `manual.md` host OS differences formatting
[changed] you can resize aoshelp now
[changed] calculator `NaN` now clears on next keypress
[changed] in the sdk, `userTheme()` is now `getTheme()`, `userSettings()` is now `getSettings()`, and `aosVersion()` is now `getVersion()`
[changed] terminal now replaces anything within graves (`) to the value of the variable within
[changed] AOS readme logo changes according to color theme
[fixed] `getSettings()` and `toBool()` functions
[fixed] `manual.md` misinformation
[fixed] splash screen not being sent to top
[fixed] terminal text not shown on light themes
[fixed] `exec` command being very stingy about slashes
[removed] `apply` button in settings