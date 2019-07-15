import os.path
from os import path

# Function Definitions
def encrypt(un, pw, act, key):
    key = strToHex(key)
    pw = strToHex(pw)
    accounts = open("accounts.txt", "a")
    accounts.write(":" + act + "\n")
    accounts.write(un + "\n")
    accounts.write(convert(pw, key, "+") + "\n")
    accounts.write("\n")
    accounts.close()
    
def strToHex(string):
    result = []
    for c in string:
        result.append(int(hex(ord(c))[2:], 16))
    return result

def hexSplit(hx):
    hxlist = []
    for i in range(int(len(hx) / 2)):
        ind = i * 2
        hxlist.append(int(hx[ind] + hx[ind+1], 16) % 128)
    return hxlist
    
def hexToStr(hx):
    return bytearray.fromhex(hx).decode("ascii")

def convert(cred, key, sign):
    if (sign == "+"):
        for i in range(len(cred)):
            cred[i] = (cred[i] + key[i % len(key)]) % 128
        tmp = ""
        for i in range(len(cred)):
            tmp += hex(cred[i])[2:]
    else:
        for i in range(len(cred)):
            cred[i] = (cred[i] - key[i % len(key)]) % 128
        tmp = ""
        for i in range(len(cred)):
            tmp += hex(cred[i])[2:]
    return tmp

def decrypt(act, key):
    accounts = open("accounts.txt", "r")
    lines = accounts.readlines()
    found = False
    for i in range(len(lines) - 1):
        line = lines[i]
        if (line[0] == ":" and line[1:len(line) - 1] == act):
            un = lines[i + 1]
            pw = hexSplit(lines[i + 2])
            found = True
            break
    if (found != True):
        print()
        print("Account not found")
    else:
        key = strToHex(key)
        print()
        print("Account for " + act + " was found")
        print("Username: " + un)
        print("Password: " + hexToStr(convert(pw, key, "-")))
    accounts.close()

        
def addAcc(service):
    print()
    print("What is the username?")
    name = input()
    print()
    print("What is the password?")
    pas = input()
    print()
    print("What is your private encryption key?")
    key = input()
    encrypt(name, pas, service, key)
    print("Account created.")

# Code
print("Welcome to Nate's Password Vault!")
if (not os.path.exists("accounts.txt")):
    tmp = open("accounts.txt", "w")
    tmp.close()
while True:
    print()
    print("Would you like to add or view an account or quit?")
    response = input().lower()
    acc = open("accounts.txt", "r")
    lines = acc.readlines()
    if response.startswith("a"):
        print()
        print("What service is the account for?")
        service = input()
        response = service.lower
        for line in lines:
            line = line.lower
        found = False
        for i in range(len(lines) - 1):
            tmpline = lines[i]
            if tmpline[1:len(tmpline) - 1] == service:
                found = True
                print("This account already exists. Overwrite?")
                response = input()
                if response.startswith("y"):
                    # remove old account
                    print("Removed old account")
                    print()
                    acc = open("accounts.txt", "w")
                    for i in range(len(lines) - 1):
                        line = lines[i]
                        if (lines[i][1:].strip("\n") != service) and (lines[i - 1][1:].strip("\n") != service) and (lines[i - 2][1:].strip("\n") != service) and (lines[i - 3][1:].strip("\n") != service):
                            acc.write(line)
                    acc.write("\n")
                    acc.close()
                    # add new account
                    addAcc(service)
        if found == False:
            addAcc(service)
    elif (response.startswith("v")):
        print()
        print("What is the service you are looking for?")
        response = input()
        print()
        print("What is your key?")
        key = input()
        decrypt(response, key)
    elif (response.startswith("q")):
        print("Exiting.")
        break