import os

class color:
    ENDC = '\033[0m'
    RED = '\033[1;31;40m'


def clear():
    os.system("cls|clear")

def banner():
    #Art by Joan G. Stark
    #jgs
    print("""       By Ego
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