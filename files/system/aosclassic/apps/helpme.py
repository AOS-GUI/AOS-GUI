helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text] {| [color]}). if a variable name is surrounded by graves (`), the variable's contents will be echoed.",
            "rm":"removes a file or folder (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-n | --notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})",
            "ver":"shows system and terminal version",
            "mkdir":"creates a directory (syntax: mkdir [path])",
            "restart":"restarts AOS (syntax: restart)",
            "mkfile":"creates a file. (syntax: mkfile [path/filename] {contents})",
            "set":"sets a value to a variable (syntax: set [var] [contents]",
            "py":"executes a python script (syntax: py [path])",
            "camel":"camelInstall CLI. run 'camel help' for more information",
            "dl":"downloads the contents of a url (syntax: dl [url] {output file path} {-s | --status})",
            "quit":"quits AOS classic (syntax: quit)"}

keys = list(helpText.keys())
keys.sort()
helpText = {i: helpText[i] for i in keys}

def main(args=[]):
    if args == []:
        print("\nAOS classic commands:\n")
        for x in helpText:
            print(x,end=" ")
        print("\nType 'help {command}' for help on that command.\n")
    elif len(args) > 0 and args[0] in helpText:
        print(helpText[args[0]])