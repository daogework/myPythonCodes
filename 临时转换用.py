from parse import compile
from parse import findall
import sys

orig_stdout = sys.stdout

_func1= compile("GAME_API {returntype} {}") 
# _func2= compile("    {returntype} {funcname}();")

printToFile = True

filename = 'export_IUser.cpp'
exprotPath = r'H:\python脚本\__fortest'

if printToFile:
    fout = open(exprotPath+'/'+filename+'', 'w')
    sys.stdout = fout

total = 0
scoreList = []

rootpath = r"H:\fll3d_server\server\gameserver\GameDll"
path = rootpath + '/' + filename
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()

resultStr = ''

isPrintResult = True

cppfileStr = ''

# print('#pragma once\n #include"ExportDll.h"\n')

def replaceParam(param):
    param = param.replace('void*','IntPtr ')
    param = param.replace('INT64','long')
    param = param.replace('UINT32','uint')
    param = param.replace('const char*','string')
    param = param.replace('char*','string')
    param = param.replace('int*','int[]')
    param = param.replace('bool*','bool[]')
    param = param.replace('const','')
    return param

def paserParam(paramstr):
    arr = str.split(paramstr, ',')
    r = ''
    for s in arr:
        s = s.strip()
        arr = str.split(s, ' ')
        r+=arr[1]+','
    r=r.rstrip(',')
    return r

lastReturnType = ''
passCount = 0 #要跳过的次数
def process(index, line, lines):
    global passCount
    global lastReturnType
    if passCount>0:
        passCount-=1
        return ''
    if line.find('//',0,5)!=-1:
        return line
    r = _func1.parse(line)
    if r != None:
        lastReturnType = r['returntype']

    isNotVoid = lastReturnType != 'void'
    addstr = ''
    if isNotVoid:
        addstr = '   auto p = mk::getUserById(userid);\n   if (!p)return 0;\n'
    else:
        addstr = '   auto p = mk::getUserById(userid);\n   if (!p)return;\n'
    if line.find('((IUser*)p)->')!=-1:
        line = line.replace('((IUser*)p)->','p->')
        line = addstr + line
    return line


##########################################

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)

main()

if isPrintResult:
    print(resultStr)


# if printToFile:
#     fout = open(exprotPath+'/export_'+filename.replace('.h','.cpp')+'', 'w')
#     sys.stdout = fout
# print('#include "export_BaseCore.h"\n#include"base/BaseCore.h"\n')
# print(cppfileStr)








