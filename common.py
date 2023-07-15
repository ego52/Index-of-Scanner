import os

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

class color:
    ENDC = '\033[0m'
    RED = '\033[1;31;40m'


def clear():
    os.system("cls|clear")

def checkVersion():
    print("")

def banner():
    #Art by Joan G. Stark
    #jgs
    version = "1.0"
    print(f"""     {version}  By Ego
       .---.
  ___ /_____\\
 /\.-`( '.' )
/ /    \_-_/_
\ `-.-"`'V'//-.
 `.__,   |// , \\
     |Ll //Ll|\ \\
     |__//   | \_\\
    /---|[]==| / /
    \__/ |   \/\/
    /_   | Ll_\|
     |`^\"\"\"^`|
     |   |   |
     |   |   |
     |   |   |
     |   |   |
     L___l___J
      |_ | _|
     (___|___)
      ^^^ ^^^""")