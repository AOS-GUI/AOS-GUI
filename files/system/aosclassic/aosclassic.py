# aos classic (like aos1 or aos2. this could be a spiritual successor to both of those!)

from files.system.aosclassic.apps import helpme

cmd = ""

print("hello, welcome to AOS classic! unfortunately, this is not fully implemented yet. look for it in a later release, though!")
print("\ntype 'help' for help.")
#print("welcome to AOS classic! type 'help' for help.")

while True:
    cmd = input("$ ")
    args = cmd.split(" ")[1:]

    if cmd.startswith("help"):
        helpme.main(args)
    elif cmd == "hello":
        print("hi!")
    elif cmd == "quit":
        break
