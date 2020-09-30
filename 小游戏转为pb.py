from parse import compile
from parse import findall
import sys
import os

orig_stdout = sys.stdout

def openfileToPrint(filename):
    sys.stdout = open(filename, 'w')

def readFileAllLines(filename, isUtf8=False):
    if isUtf8:
        return open(filename,mode='r', encoding="utf-8" ).readlines()
    else:
        return open(filename,mode='r').readlines()

_package= compile("package {pkgname};") 
_message= compile("message {msgname}")

printToFile = True

gameBaseName = 'DDZ'
clname = 'CL'+gameBaseName
filename = f'{clname}.proto'
filenameRaw = os.path.splitext(filename)[0]
fileExt = os.path.splitext(filename)[1]

exportfilename = filenameRaw+'Handler'
gameRootName = r'H:\fll3d_server\server\gameserver\Game'+gameBaseName

exportPath = gameRootName + r'\handler'
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



#转换stdafx.h
stdafx_h_path = gameRootName + '/app/' + 'stdafx.h'
lines = readFileAllLines(stdafx_h_path)
isConverted = False
for line in lines:
    if 'pb/' in line:
        isConverted = True
        break
if not isConverted:
    if printToFile:
        openfileToPrint(stdafx_h_path)
    for line in lines:
        if 'jb/' in line:
            continue
        if '#define GAME_SERVER_NAME' in line:
            print(f'#include "pb/CL{gameBaseName}.pb.h"\n'+line)
            continue
        print(line.replace('\n',''))


NotifyImpl_path = gameRootName + '/app/' + 'NotifyImpl.cpp'
lines = readFileAllLines(NotifyImpl_path)

skiplinecount = 0
isConverted = False
for line in lines:
    if clname+'Handler::init();' in line:
        isConverted = True
        break
if not isConverted:
    if printToFile:
        openfileToPrint(NotifyImpl_path)
    for line in lines:
        if skiplinecount > 0:
            skiplinecount-=1
            continue
        if '#include "stdafx.h"' in line:
            print('#include "stdafx.h"\n#include "handler/'+clname+'Handler.h"\n')
            continue
        if 'onApplicationStart' in line:
            print(line.replace('\n','')+'\n{')
            print('    '+clname+'Handler::init();')
            skiplinecount = 1
            continue
        print(line.replace('\n',''))



def paserFunc(param, index, lines, _memcpy, skiplinecount):
    _paser = compile('{space}'+param+'.{value1} = {value2};')
    _setstr = compile('{space}StrSafeCopy({param}.{value1}, {value2});')
    for i in range(index+1, len(lines)):
        line = lines[i]
        if '}' in line:
            break
        else:
            skiplinecount+=1
        r = _paser.parse(line)
        if not r is None:
            value1 = r['value1']
            value2 = r['value2']
            space = r['space']
            print(space + param +'->set_'+value1+'('+value2+');')
            continue
        r = _setstr.parse(line)
        if not r is None:
            value1 = r['value1']
            value2 = r['value2']
            space = r['space']
            print(space + param +'->set_'+value1+'('+value2+');')
            continue
        r = _memcpy.parse(line)
        if not r is None:
            pb = r['pb']
            value1 = r['value1']
            value2 = r['value2']
            space = r['space']
            print(space + 'for (auto v : '+value2+') {')
            print(space + '    '+pb+'->add_'+value1+'(v);')
            print(space+'}')
            continue
        print(line.replace('\n',''))
    return skiplinecount


def convertLines(lines):
    _paserack = compile('{space}ack.{value1} = {value2};')
    _paserntf = compile('{space}ntf.{value1} = {value2};')
    _func1 = compile('{returnvalue} {classname}::{funcname}({jbtype}& {param})')
    _func2 = compile('{space}{void} {funcname}({jbtype}& {param});')
    _func3 = compile('{space}void {funcname}({jbtype}& {param})')
    _memcpy = compile('{space}memcpy({pb}.{value1}, {value2}, sizeof({ack.result}));')
    skiplinecount = 0
    for index, line in enumerate(lines):
        if skiplinecount > 0:
            skiplinecount-=1
            continue

        if clname+'::' in line:#说明处理过了
            print(line.replace('\n',''))
            continue
        if clname in line and ('Ack' in line or 'Ntf' in line):
            line = line.replace(clname,clname+'::')
            print(line.replace('\n',''))
            continue
        if 'MAKE_PROTO_EMPTY' in line:
            continue
        if 'ack.' in line :
            r = _paserack.parse(line)
            if not r is None:
                value1 = r['value1']
                value2 = r['value2']
                space = r['space']
                print(space + 'ack.set_'+value1+'('+value2+');')
                continue
            r = _memcpy.parse(line)
            if not r is None:
                pb = r['pb']
                value1 = r['value1']
                value2 = r['value2']
                space = r['space']
                print(space + 'for (auto v : '+value2+') {')
                print(space + '    '+pb+'.add_'+value1+'(v);')
                print(space+'}')
                continue
        if 'ntf.' in line :
            r = _paserntf.parse(line)
            if not r is None:
                value1 = r['value1']
                value2 = r['value2']
                space = r['space']
                print(space + 'ntf.set_'+value1+'('+value2+');')
                continue
        if clname in line:
            r = _func1.parse(line)
            if not r is None:
                line = line.replace(clname,clname+'::').replace('&','*')
                print(line.replace('\n',''))
                param = r['param']
                skiplinecount = paserFunc(param, index, lines, _memcpy, skiplinecount)
                continue

            r = _func2.parse(line)
            if not r is None:
                line = line.replace(clname,clname+'::').replace('&','*')
                print(line.replace('\n',''))
                continue
            r = _func3.parse(line)
            if not r is None:
                line = line.replace(clname,clname+'::').replace('&','*')
                print(line.replace('\n',''))
                param = r['param']
                skiplinecount = paserFunc(param, index, lines, _memcpy, skiplinecount)
                continue
            
        print(line.replace('\n','').replace(' max(',' std::max('))



def batchConvert(filepathList):
    for fpath in filepathList:
        file = open(fpath,mode='r')
        lines = file.readlines()
        file.close()
        if printToFile:
            openfileToPrint(fpath)
            convertLines(lines)

filepathList = [
    gameRootName + '/model/user/UserDataComponent.cpp',
    gameRootName + '/model/user/UserHelper.cpp',
]

batchConvert(filepathList)