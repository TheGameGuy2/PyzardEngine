import os
print("type 'help' for more info")
commands=["setup","build","help"]
while True:
    s_inp=input(">")
    s_inp=s_inp.lower()

    if not s_inp.split(" ")[0] in commands:
        print("Invalid command")
        continue
    if s_inp=="setup":
        os.system("pip install pygame")
        os.system("pip install pyinstaller")
    if s_inp.startswith("build"):
        dir=s_inp.split(" ")[1]
        os.system(f"pyinstaller -w --onefile {dir}")
    if s_inp=="help":
        print(f"Commands: {commands} | see docs for more info")
        
