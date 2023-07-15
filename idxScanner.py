#Libs
import re
import queue
import urllib3
import requests
import threading
#Files
import common
import argsReader

def symLinkTester(_url):
    """Test url with last path twice

    Args:
        _url (String): web link

    Returns:
        bool: value of response 1 length equal to response 2 length
    """
    path = _url.split("/")[-1]
    responseF = requests.get(_url, headers=common.headers, timeout=(20, 20), verify=False)
    responseS = requests.get(f"{_url}/{path}/", headers=common.headers, timeout=(20, 20), verify=False)
    return len(responseF.content) == len(responseS.content)

def isFile(response):
    """Check if title contains Index of

    Args:
        response (requests.response): response of web request

    Returns:
        bool: value of index of if is in title
    """
    try:
        title = re.findall(r"<title>(.*)</title>", response.content.decode())
    except:
        return True
    if title == []:
        return True
    try:
        return not "index of" in title[0].lower()
    except:
        print(response.content.decode())
        print(title)
        exit()

def getPaths(response):
    """Use regex to get paths (directories/files)

    Args:
        response (requests.response): web response

    Returns:
        String[]: array of paths
    """
    try:
        findings = re.findall(r"<tr><td valign=\"top\">(&nbsp;|<img src=\"[/\w+\.]+\" alt=\"([\[\w+\s\]]*)\">)*</td><td><a href=\"([/\w\.-]*)\">.*</td><td>&nbsp;</td></tr>", response.content.decode())
        if findings != []:
            # print("Type 1")
            return findings
            
        findings = re.findall(r" alt=\"\[[\w\s]+\]\"> <a href=\"(.*)\">.*</a>[\s\d\w:-]+-", response.content.decode())
        if findings != []:
            # print("Type 2")
            return findings
        
        findings = re.findall(r"<tr[\s\w\"-=]*><td[\s\d\w\"-=]*><a href=\"(.*)\"><img class=\"icon\" src=\"/[\w/\d\.-]+\".*</td></tr>", response.content.decode())
        if findings != []:
            # print("Type 3")
            return findings
        
        findings = re.findall(r"<a href=\"(.*)\">.*</a>[\s\d\w:-]+-", response.content.decode())
        if findings != []:
            # print("Type 4")
            return findings
        
        findings = re.findall(r"<tr><td><a href=\"(.*)\">.*</a></td>", response.content.decode())
        if findings != []:
            # print("Type 5")
            pass
        return findings
    except:
        try:
            return re.findall(r"<a href=\"(.*)\">.*</a>[\s\d\w:-]+-", response.content.decode())
        except:
            print("Interesting...")
            exit()

def isEmptyIdx(_url):
    """Check if it is index of page next is get links and if there is new directories

    Args:
        _url (String): web links

    Returns:
        int: -1 if it is a file 0 incase of many files 1 incase of empty index of
    """
    try:
        response = requests.get(_url, headers=common.headers, stream=True, timeout=(5, 5), verify=False)
    except:
        return -1
    if isFile(response):
        filePaths.append(_url.split(rooturl)[1])
        return -1
    findings = getPaths(response)
    return len(findings) == 1

def getContents(_url, toTry=True):
    """Loop function to read index of and store found paths (directories/files)

    Args:
        _url (String): web link
        toTry (bool): Default is True incase of first time link False incase of second time
    """
    response = requests.get(_url, headers=common.headers, timeout=(20, 20), verify=False)
    findings = getPaths(response)
    for finding in findings:
        try:
            if type(finding) != type(""):
                finding = finding[2]
        except:
            pass
        if finding[0] == "/":
            path = finding
        else:
            path = getCurrentPath(_url + finding)
        if not path in checkedPaths:
            if path.split("/")[-2] in bypassDir:
                continue
            if path.split("/")[-1] in foundFile or path.split("/")[-2] in foundDir or path.split("/")[-1].split(".")[-1] in foundFileType:
                print(f"{common.color.RED}{rooturl + path}{common.color.ENDC}")
            else:
                print(rooturl + path)
            isIdx = isEmptyIdx(rooturl + path)
            if isIdx == -1:
                continue
            elif isIdx != 1:
                checkedPaths.append(path)
                if not symLinkTester(rooturl + path) or toTry:
                    getContents(rooturl + path, False)

def getCurrentPath(_url):
    return _url.split(rooturl)[-1]

def argsChecker():
    """Set global variables and check if args are set properly
    """
    global url, rooturl
    pattern = re.compile("^(http|https)://(\w+|\.)+(/|.*)$")
    if pattern.match(argsReader.args.url) is None:
        print("Not a valid url")
        exit()
    url = argsReader.args.url
    rooturl = url.split("//")[0] + "//" + url.split("//")[1].split("/")[0]
    checkedPaths.append(getCurrentPath(url))

urllib3.disable_warnings()
if __name__ == "__main__":
    checkedPaths = []
    filePaths = []
    
    foundDir = []
    f = open("config/important/directories.idxs", "r+")
    lines = f.readlines()
    for line in lines:
        foundDir.append(line.strip())
    f.close()
    
    foundFile = []
    f = open("config/important/files.idxs", "r+")
    lines = f.readlines()
    for line in lines:
        foundFile.append(line.strip())
    f.close()

    foundFileType = []
    f = open("config/important/filetypes.idxs", "r+")
    lines = f.readlines()
    for line in lines:
        foundFileType.append(line.strip())
    f.close()

    bypassDir = []
    f = open("config/bypass/directories.idxs", "r+")
    lines = f.readlines()
    for line in lines:
        bypassDir.append(line.strip())
    f.close()

    argsChecker()
    getContents(url)

    # f = open("found.txt", "r")
    # if f.readlines() == []:
    #     input("Rewrite file [w,a]")
    # f.close()

    f = open(argsReader.args.save, "a")
    f.write("Directories:\n")
    for path in checkedPaths:
        f.write(f"{path}\n")

    f.write("Files:\n")
    for path in filePaths:
        f.write(f"{path}\n")
    f.close()
