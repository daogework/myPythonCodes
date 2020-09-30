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

def handleMemcpy(r):
    pb = r['pb']
    value1 = r['value1']
    value2 = r['value2']
    space = r['space']
    print(space + 'for (auto v : '+value2+') {')
    print(space + '    '+pb+'.add_'+value1+'(v);')
    print(space+'}')

def convertLines(lines):
    _paserack = compile('{space}ack.{value1} = {value2};')
    _paserntf = compile('{space}ntf.{value1} = {value2};')
    _func1 = compile('{returnvalue} {classname}::{funcname}({jbtype}& {param})')
    _func2 = compile('{space}{void} {funcname}({jbtype}& {param});')
    _func3 = compile('{space}void {funcname}({jbtype}& {param})')
    _memcpy = compile('{space}memcpy({pb}.{value1}, {value2}, {size});')
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
                handleMemcpy(r)
                continue
        if 'ntf.' in line :
            r = _paserntf.parse(line)
            if not r is None:
                value1 = r['value1']
                value2 = r['value2']
                space = r['space']
                print(space + 'ntf.set_'+value1+'('+value2+');')
                continue
            r = _memcpy.parse(line)
            if not r is None:
                handleMemcpy(r)
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
    # gameRootName + f'/model/{gameBaseName}/{gameBaseName}StateBalance.cpp',
    # gameRootName + f'/model/{gameBaseName}/{gameBaseName}StateBalance.h',
    # gameRootName + '/model/user/UserHelper.cpp',
    # gameRootName + f'/model/{gameBaseName}/{gameBaseName}StateCompareCards.cpp',
    # gameRootName + '/model/user/UserDataComponent.cpp',
    # gameRootName + f'/model/{gameBaseName}/{gameBaseName}Controller.h',
    # gameRootName + f'/model/{gameBaseName}/{gameBaseName}Controller.cpp',

    gameRootName + f'/model/{gameBaseName}/{gameBaseName}StateDispatching.h',
    gameRootName + f'/model/{gameBaseName}/{gameBaseName}StateDispatching.cpp',
    # gameRootName + f'/model/Packet/Packet.cpp',
    # gameRootName + f'/model/Robot/RobotComponent.h',
    # gameRootName + f'/model/Robot/RobotComponent.cpp',
    # gameRootName + f'/model/match/matchhelper.h',
    # gameRootName + f'/model/match/matchhelper.cpp',
]

batchConvert(filepathList)