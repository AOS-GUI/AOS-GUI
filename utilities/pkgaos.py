#! /bin/python3

# this script packages AOS-GUI for distribution. please run this from the parent dir!

import shutil
import os
os.chdir("..")
CWD = os.getcwd()

ans = input("\n\n-- pkgaos.py --\n\nthis python script packages AOS for distribution. it assumes that you are inside of the /utilities/ folder. would you like to continue? [y/n] ")
if ans.lower()=="y":
    print("copying dir into new folder...")
    shutil.copytree(CWD, ".AOSGUI-PKG")
    print("removing all unneeded user data...")
    shutil.rmtree(CWD+"/.AOSGUI-PKG/files/home/")
    os.mkdir(CWD+"/.AOSGUI-PKG/files/home/")

    for f in os.listdir(CWD+"/.AOSGUI-PKG/files/apps/"):
        if f.endswith(".py"):
            os.remove(CWD+"/.AOSGUI-PKG/files/apps/"+f)

    shutil.rmtree(CWD+"/.AOSGUI-PKG/files/apps/assets/")
    os.mkdir(CWD+"/.AOSGUI-PKG/files/apps/assets/")
    os.remove(CWD+"/.AOSGUI-PKG/files/system/data/user/data.aos")
    open(CWD+"/.AOSGUI-PKG/files/system/data/user/autorun.aos","w+")
    open(CWD+"/.AOSGUI-PKG/files/system/data/user/desktop.aos","w+")
    open(CWD+"/.AOSGUI-PKG/files/system/data/user/menubar.aos","w+")
    open(CWD+"/.AOSGUI-PKG/files/system/data/user/terminal.aos","w+")

    print("removing git data...")
    shutil.rmtree(CWD+"/.AOSGUI-PKG/.git/")
    os.remove(CWD+"/.AOSGUI-PKG/.gitattributes")
    os.remove(CWD+"/.AOSGUI-PKG/.gitignore")

    print("removing everything else...")
    # os.remove(CWD+"/.AOSGUI-PKG/pkgaos.py")
    for dirpath, dirnames, files in os.walk(CWD+"/.AOSGUI-PKG/"):
        for dirname in dirnames:
            if dirname == "__pycache__":
                pycacheDir = os.path.join(dirpath, dirname)
                shutil.rmtree(pycacheDir)

    print("zipping...")
    shutil.make_archive("AOS-GUI", "zip", CWD+"/.AOSGUI-PKG/")

    print("cleaning up...")
    shutil.rmtree(CWD+"/.AOSGUI-PKG/")

    print("done!")
