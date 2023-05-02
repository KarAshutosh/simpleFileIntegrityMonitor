# import os
# import hashlib
# import time
#
# prevHashFile = open('lastHash.txt')
# lastHash = prevHashFile.read()
#
# if lastHash != "":
#     hashFile = open('currentHash.txt', 'w')
#     newRun = False
# else:
#     print('No previous hash file found, generating hashes')
#     prevHashFile.close()
#     hashFile = open('lastHash.txt', 'w')
#     newRun = True
#
# hashList = []
#
# for root, dirs, files in os.walk('.', topdown=True):
#     for name in files:
#         item = (os.path.join(root, name))
#         if './sys' in item or './dev' in item or './proc' in item or './run' in item or './tmp' in item or './var/lib' in item or './var/run' in item:
#             continue
#         else:
#             try:
#                 File = open(item, 'r').read()
#                 hashFile = hashlib.sha256(File.encode('utf-8')).hexdigest()
#                 timeStamp = time.time()
#                 hashList.append(str(timeStamp) + ':' + item + ':' + str(hashFile))
#             except:
#                 continue
#     for name in dirs:
#         item = (os.path.join(root, name))
#         if './sys' in item or './dev' in item or './proc' in item or './run' in item or './tmp' in item or './var/lib' in item or './var/run' in item:
#             continue
#         else:
#             try:
#                 File = open(item, 'r').read()
#                 hashFile = hashlib.sha256(File.encode('utf-8')).hexdigest()
#                 timeStamp = time.time()
#                 hashList.append(str(timeStamp))
#             except:
#                 continue
#
# for item in hashList:
#     hashFile = open('currentHash.txt', 'w')
#     hashFile.write(str(item))
#     hashFile.write('\n')
# if newRun:
#     print('Hashes made, program will now  compare future runs with this')
#     hashFile.close()
# else:
#     oldHashList = lastHash.split('\n')
#     fileDict = {}
#     newFileDict = {}
#
#     for i in oldHashList[0:-1]:
#         fileDict[i.split(":")[1]] = i.split(':')[2]
#     for j in hashList[0:-1]:
#         newFileDict[j.split(":")[1]] = j.split(':')[2]
#
#     for key in newFileDict:
#         if key not in fileDict:
#             print("New File+ str(key) + found.")
#             continue
#         elif newFileDict[key] != fileDict[key]:
#             print("File + str(key) + modified.")
#             continue
#         else:
#             continue
#     prevHashFile.close()
#     prevHashFile = open('lastHash.txt', 'w')
#     for item in hashList:
#         prevHashFile.write(item)
#         prevHashFile.write("\n")
#     hashFile.close()
#     prevHashFile.close()


import hashlib
import os.path
from os import listdir
from os.path import isfile, join

#getting all the files names at the folder
def nameOfFiles():
    filesNames = [f for f in listdir("FIM/Files") if isfile(join("FIM/Files", f))]
    return(filesNames)
nameOfFiles()

# the main function that open all the files at the folder,
#calculate the digest of each file and append to a final file
#that will later save to a txt
def main():
    filesHash = ''
    sha512 = hashlib.sha512()
    for i in filesNames:
        with open("FIM/files/"+ i, "rb") as f:
            while True:
                data = f.read()
                if not data:
                    break
                sha512.update(data)
                filesHash+=(sha512.hexdigest())
    return(filesHash)

def createControlFile():
    with open('fileControlData.txt','w',encoding = 'utf-8') as f:
        for i in fileControl: f.write(i)
    print("File generated, Everything is OK my brother!")

filesNames = nameOfFiles()
fileControl = main()
if os.path.exists("fileControlData.txt") is True:
    with open('fileControlData.txt','r',encoding = 'utf-8') as file:
        file = file.read()
        if file == fileControl:
            print("The files are intact!")
        else:
            if len(fileControl)> len(file):
                answer = input("A file was added, do you wanna to recreate the control File?(y/n)").lower()
                if answer == "y":
                    createControlFile()
            elif len(fileControl)< len(file):
                answer = input("A file was removed, do you wanna to recreate the control File?(y/n)").lower()
                if answer == "y":
                    createControlFile()
            else:
                answer = input("The files have been changed, do you wanna to recreate the control File?(y/n)").lower()
                if answer == "y":
                    createControlFile()
else:
    createControlFile()






















