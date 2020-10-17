from parse import compile
from parse import findall
import sys
import os
import time

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

gameBaseName = 'FQZS'
clname = 'CL'+gameBaseName
filename = f'{clname}.proto'
filenameRaw = os.path.splitext(filename)[0]
fileExt = os.path.splitext(filename)[1]


exportPath = r'H:\fll3d_subGames\FQZS_Lua\Assets\Scripts\Lua\protobuffer\PBSender.lua'

frompath = r"H:\fll3d_support\protobuf\config"

fout = None

if printToFile:
    fout = open(exportPath, 'w', encoding="utf-8")
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

print(r'''--以下是由.proto自动生成的代码
local print = print
local debug = debug
local logError,logWarning,log = logError,logWarning,log

local PBHelper = require'protobuffer.PBHelper'

_ENV = {}

local function LogE(str)
    logError('[PBSender]'..str..'\n'..debug.traceback())
end

local function LogW(str)
    logWarning('[PBSender]'..str..'\n'..debug.traceback())
end

local function Log(str)
    log('[PBSender]'..str..'\n'..debug.traceback())
end

local Send = PBHelper.Send
local AsyncRequest = PBHelper.AsyncRequest
''')

msgnameList = []
pkgname = ''
passCount = 0 #要跳过的次数
def process(index, line, lines):
    global passCount
    global pkgname
    if passCount>0:
        passCount-=1
        return ''
    r = _package.parse(line)
    if not r is None:
        pkgname = r['pkgname']
        return ''
    r = _message.parse(line)
    if not r is None:
        msgname = r['msgname']
        t = {'msgname':msgname}
        msgnameList.append(t)
        paserProtoParam(index+1, lines, t)
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


for msg in msgnameList:
    msgname = msg['msgname']
    params = msg['params']
    if 'Req' in msgname:
        funcparam = ''
        senddataparam = ''
        for param in params:
            name = param['name']
            funcparam += ', '+name
            senddataparam += name+' = '+name+', '

        funcdefine = f'function Send_{msgname}(callback{funcparam})'
        senddatadefine = '    local senddata = {'+senddataparam+'}'
        print(funcdefine)
        print(senddatadefine)
        reqname ="'"+pkgname+'.'+msgname+"'"
        ackname = reqname.replace('Req','Ack')
        print(f'    AsyncRequest({reqname},senddata,{ackname},callback)')
        print('end\n')











print('\nreturn _ENV')

if fout:
    fout.flush()
# def batchConvert(filepathList):
#     for fpath in filepathList:
#         file = open(fpath,mode='r')
#         lines = file.readlines()
#         file.close()
#         if printToFile:
#             openfileToPrint(fpath)
#             convertLines(lines)

# filepathList = [
#     gameRootName + '/model/user/UserDataComponent.cpp',
#     gameRootName + '/model/user/UserHelper.cpp',
# ]

# batchConvert(filepathList)