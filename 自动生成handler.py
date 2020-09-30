from parse import compile
from parse import findall
import sys
import os

orig_stdout = sys.stdout

_package= compile("package {pkgname};") 
_message= compile("message {msgname}")

printToFile = True

filename = 'CLZJH.proto'
filenameRaw = os.path.splitext(filename)[0]
fileExt = os.path.splitext(filename)[1]
exportfilename = filenameRaw+'Handler'
exportPath = r'H:\fll3d_server\server\gameserver\GameZJH\handler'
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
printToCpp('#include "model/user/UserDataComponent.h"')
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
            t = {'msgname':msgname}
            msgnameList.append(t)
            paserProtoParam(index+1, lines, t)
            print(f'    static void on{pkgname}{msgname}(IUser* user, {pkgname}::{msgname}& proto);')
            
        return ''
    return ''

def paserProtoParam(index, lines, t):
    paramslist = t['params'] = []
    _paser = compile("    {type} {name} = {}; {}")
    for i in range(index, len(lines)):
        line = lines[i]
        isrepeated = False
        if 'repeated ' in line:
            isrepeated = True
            line = line.replace('repeated ', '')
        r = _paser.parse(line)
        if not r is None:
            t = {
                'type':r['type'],
                'name':r['name'],
                'isrepeated':isrepeated,
            }
            paramslist.append(t)
        if '}' in line:
            break

##########################################

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)

main()



print('};')

for t in msgnameList:#//init函数内容
    msgname = t['msgname']
    params = t['params']
    printToCpp(f'    mk::registerPBHandler<{pkgname}::{msgname}>(on{pkgname}{msgname});')
printToCpp('}\n')

for t in msgnameList:
    msgname = t['msgname']
    params = t['params']
    paramsstr = ''
    for index, p in enumerate(params):
        end = ''
        if index != len(params)-1:
            end = ', '
        paramsstr += 'proto.' + p['name'].lower() + '()' + end

    printToCpp(f'void {pkgname}Handler::on{pkgname}{msgname}(IUser* user, {pkgname}::{msgname}& proto)')
    printToCpp('{')
    printToCpp('    auto com = user->getComponent<UserDataComponent>();')
    if len(params)>0:
        printToCpp(f'    com->process{msgname}({paramsstr});')
    else:
        printToCpp(f'    com->process{msgname}();')
    printToCpp('}\n')

if printToFile:
    fout = open(exportPath+'/'+exportfilename+'.cpp', 'w')
    sys.stdout = fout
print(cppfilestr)










