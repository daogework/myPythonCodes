from parse import compile
from parse import findall
import sys

orig_stdout = sys.stdout

_class= compile("class {classname}")
# _func1= compile("    virtual {returntype}   {funcname}({param}) = 0;") 
# _func2= compile("    virtual {returntype}   {funcname}() = 0;")
_func1= compile("    virtual {returntype} {funcname}({param}) = 0;") 
_func2= compile("    virtual {returntype} {funcname}() = 0;")

printToFile = True

filename = 'IUser.h'
exprotPath = 'H:\\fll3d_server\\server\\gameserver\\GameDll'

if printToFile:
    fout = open(exprotPath+'/export_'+filename+'', 'w')
    sys.stdout = fout

total = 0
scoreList = []

rootpath = "H:\\fll3d_server\\server\\gameserver\\base\\base"
path = rootpath + '/' + filename
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()

resultStr = ''

isPrintResult = True

cppfileStr = ''

print('#pragma once\n #include"ExportDll.h"\n')

def paserParam(paramstr):
    arr = str.split(paramstr, ',')
    r = ''
    for s in arr:
        s = s.strip()
        arr = str.split(s, ' ')
        r+=arr[1]+','
    r=r.rstrip(',')
    return r

classname = ''

passCount = 0 #要跳过的次数
def process(index, line, lines):
    global passCount
    global cppfileStr
    global classname
    if passCount>0:
        passCount-=1
        return ''
    r = _class.parse(line)
    if not r is None:
        classname = r['classname']


    r = _func1.parse(line)
    if not r is None:
        returntype = r['returntype']
        funcname = r['funcname']
        funcname = funcname.replace(' ', '')
        param = r['param']
        zhushi = ''
        if param.find('T&')!=-1 or param.find('T*')!=-1:
            zhushi = '//'
        param = param.replace('fmt, ...','str')
        param = param.replace('std::string &','char* ')
        param = param.replace('std::string&','char* ')
        param = param.replace('&','*')
        cppfileStr +=  zhushi+'GAME_API '+returntype+' '+classname+'_'+funcname+'(void* p,'+param+'){\n '
        paars = param.split(',')
        paramstr = ''
        counter = 0
        for p in paars:
            counter+=1
            tt = p.split(' ')
            if counter>=len(paars):
                paramstr += tt[len(tt)-1]
            else:
                paramstr += tt[len(tt)-1]+', '
        paramstr = paramstr.replace('[]','')
        pointerConvert = '(('+classname+'*)p)->'
        cppfileStr += zhushi+'  return '+pointerConvert+funcname+'('+paramstr+');\n'
        cppfileStr += zhushi+'}\n'
        return zhushi+'GAME_API '+returntype+' '+classname+'_'+funcname+'(void*,'+param+');\n'
    r = _func2.parse(line)
    if not r is None:
        returntype = r['returntype']
        funcname = r['funcname']
        funcname = funcname.replace(' ', '')
        cppfileStr +=  'GAME_API '+returntype+' '+classname+'_'+funcname+'(void* p){\n '
        pointerConvert = '(('+classname+'*)p)->'
        cppfileStr += '  return '+pointerConvert+funcname+'();\n '
        cppfileStr += '}\n'
        return 'GAME_API '+returntype+' '+classname+'_'+funcname+'(void*);\n'
   
    return ''


##########################################

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)

main()

if isPrintResult:
    print(resultStr)


if printToFile:
    fout = open(exprotPath+'/export_'+filename.replace('.h','.cpp')+'', 'w')
    sys.stdout = fout
print('#include "export_IUser.h"\n#include"base/IUser.h"\n')
print(cppfileStr)








