from parse import compile
from parse import findall
import sys

orig_stdout = sys.stdout

_func1= compile("{GAME_API} {returntype} {funcname}({param});") 
# _func2= compile("    {returntype} {funcname}();")

printToFile = True

filename = 'export_IUser.h'
exprotPath = r'H:\python脚本\__fortest'

if printToFile:
    fout = open(exprotPath+'/'+filename+'.cs', 'w')
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

passCount = 0 #要跳过的次数
def process(index, line, lines):
    global passCount
    if passCount>0:
        passCount-=1
        return ''
    if line.find('//',0,5) != -1:
        return ''
    r = _func1.parse(line)
    if not r is None:
        returntype = r['returntype']
        returntype = replaceParam(returntype)
        funcname = r['funcname']
        funcname = funcname.replace(' ', '')
        param = r['param']
        param = replaceParam(param)
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
        headline = '[DllImport(dllName, CallingConvention = CallingConvention.Cdecl)]\n'
        return (headline+'public static extern '+returntype+' '+funcname+'('+param+');\n\n').replace('char*','string ')
    # r = _func2.parse(line)
    # if not r is None:
    #     returntype = r['returntype']
    #     funcname = r['funcname']
    #     funcname = funcname.replace(' ', '')
    #     cppfileStr +=  'GAME_API '+returntype+' Exported_'+funcname+'(){\n '
    #     cppfileStr += '  return mk::'+funcname+'();\n '
    #     cppfileStr += '}\n'
    #     return 'GAME_API '+returntype+' Exported_'+funcname+'();\n'
   
    return ''


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








