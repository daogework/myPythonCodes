from parse import compile
from parse import findall
import sys
import os

orig_stdout = sys.stdout

_package= compile("package {pkgname};") 
_message= compile("message {msgname}")

printToFile = True

filename = 'CLSHZ.proto'
filenameRaw = os.path.splitext(filename)[0]
fileExt = os.path.splitext(filename)[1]
exportfilename = filenameRaw+'Handler'
exportPath = r'H:\fll3d_server\server\gameserver\GameShz\handler'
frompath = r"H:\fll3d_support\protobuf\config"

if printToFile:
    fout = open(exportPath+'/'+exportfilename+'.h', 'w')
    sys.stdout = fout

total = 0
scoreList = []


path = frompath + '/' + filename
file = open(path,mode='r', encoding="utf-8" )
lines = file.readlines()

resultStr = ''

cppfilestr = ''

def printToCpp(sadd):
    global cppfilestr
    cppfilestr += (sadd + '\n')

def paserParam(paramstr):
    arr = str.split(paramstr, ',')
    r = ''
    for s in arr:
        s = s.strip()
        arr = str.split(s, ' ')
        r+=arr[1]+','
    r=r.rstrip(',')
    return r

print('#pragma once\n//以下是由.proto自动生成的代码')
printToCpp('//以下是由.proto自动生成的代码\n#include "stdafx.h"')
msgnameList = []
pkgname = ''
passCount = 0 #要跳过的次数
def process(index, line, lines):
    global passCount
    global pkgname
    if passCount>0:
        passCount-=1
        return ''
    #_package= compile("package {pkgname};") 
    #_message= compile("message {msgname}")
    r = _package.parse(line)
    if not r is None:
        pkgname = r['pkgname']
        print(f'class {pkgname}Handler')
        print('{\npublic:\n    static void init();\n')
        printToCpp(f'#include "{pkgname}Handler.h"\n')
        printToCpp(f'void {pkgname}Handler::init()')
        printToCpp('{')
        return ''
    r = _message.parse(line)
    if not r is None:
        msgname = r['msgname']
        if 'Req' in msgname:
            msgnameList.append(msgname)
            print(f'    static void on{pkgname}{msgname}(IUser* user, {pkgname}::{msgname}& proto);')
            
        return ''
    return ''


##########################################

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)

main()



print('};')

for msgname in msgnameList:#//init函数内容
    printToCpp(f'    mk::registerPBHandler<{pkgname}::{msgname}>(on{pkgname}{msgname});')
printToCpp('}\n')

for msgname in msgnameList:
    printToCpp(f'void {pkgname}Handler::on{pkgname}{msgname}(IUser* user, {pkgname}::{msgname}& proto)')
    printToCpp('{')
    printToCpp(f'    user->sendComponentMessage(\n    "UserDataComponent","process{msgname}", &proto);')
    printToCpp('}\n')

if printToFile:
    fout = open(exportPath+'/'+exportfilename+'.cpp', 'w')
    sys.stdout = fout
print(cppfilestr)










