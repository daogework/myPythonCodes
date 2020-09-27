from parse import compile
from parse import findall
import sys

orig_stdout = sys.stdout

_class = compile("class {classname} : {classbasename} {") 
_classNoBase = compile("public class {classname} {") 
_MemberVariables = compile("    {visibility} {type} {name} { get; set; }") 
_MemberVariables2 = compile("    {visibility} {type} {name};") 
_MemberFunction = compile("    {visibility} {returntype} {funcname}({param}) {") 

printToFile = False

filename = 'MessageBoxModule.cs'
exprotPath = r'H:\python脚本\__fortest'

if printToFile:
    fout = open(exprotPath+'/export_'+filename+'.lua', 'w')
    sys.stdout = fout

total = 0
scoreList = []

rootpath = r"H:\fll3d_plaza\client\Plaza\Assets\Scripts\GameLogic\Module"
path = rootpath + '/' + filename
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()
allfileText = ''
for line in lines:
    nospaceline = line.replace(' ','')
    if nospaceline.find('//',0,3)!=-1:
        continue #跳过注释行
    allfileText += line

resultStr = ''

isPrintResult = True

cppfileStr = ''

# print('#pragma once\n #include"ExportDll.h"\n')

def paserParam(paramstr):
    arr = str.split(paramstr, ',')
    r = ''
    for s in arr:
        s = s.strip()
        arr = str.split(s, ' ')
        r+=arr[1]+','
    r=r.rstrip(',')
    return r




##########################################
def Find_matching_brackets(index, strv, start, end):#寻找匹配的括号
    count = 0
    isFoundFirst = False
    startindex = -1
    for i in range(index,len(strv)):
        s = strv[i]
        if s==start:
            count+=1
            if not isFoundFirst:
                startindex = i
                isFoundFirst = True
        elif s==end and isFoundFirst:
            count-=1
        if count==0 and isFoundFirst:
            return startindex, i
    return -1



def paserMemberVariables(classdic, classContentStrLines):
    memberVariablesList = []
    classdic['memberVariables'] = memberVariablesList
    for line in classContentStrLines:
        r = _MemberVariables.parse(line)
        if not r is None:
            type_ = r['type']
            name = r['name']
            visibility = r['visibility']
            dic = {'type':type_,'name':name,'visibility':visibility}
            memberVariablesList.append(dic)
        r = _MemberVariables2.parse(line)
        if not r is None:
            type_ = r['type']
            type_ = type_.replace(' ','')
            if type_=='':
                continue
            name = r['name']
            visibility = r['visibility']
            dic = {'type':type_,'name':name,'visibility':visibility}
            memberVariablesList.append(dic)

def paserParams(funcdic, params):
    paramList=[]
    funcdic['paramList'] = paramList
    paramstrlist=[]
    if ',' in params:
        paramstrlist = params.split(',')
    else:
        paramstrlist.append(params)

    for params in paramstrlist:
        slist = params.split(' ')
        paramdic={
            'type':slist[0],
            'name':slist[1],
        }
        paramList.append(paramdic)

def paserSwitchCaseBlock(switchBlockBlockdic,switchcontentstr):
    caseBlockList = []
    switchBlockBlockdic['caseBlockList'] = caseBlockList
    startindex = 0
    while True:
        index = switchcontentstr.find('case', startindex)
        if index==-1:
            break
        startindex = index+1
        index2 = switchcontentstr.find(':', index)
        assert(index2!=-1)
        caseValue = switchcontentstr[index+5:index2]
        caseBlockdic = {
            'caseValue':caseValue,
        }
        
        caseBlockList.append(caseBlockdic)
        caseContentstr = ''
        nextCaseIndex = switchcontentstr.find('break', index2)
        if index2==-1:
            caseContentstr = switchcontentstr[index2+2:]
        else:
            caseContentstr = switchcontentstr[index2+2:nextCaseIndex-1]
        paserBlock(caseBlockList, caseContentstr)
        
        
        

def parseSwitchBlock(blockList, contentStr):
    index = contentStr.find('switch')
    if index!=-1:
        sindex, eindex = Find_matching_brackets(index, contentStr, '{','}')
        switchstr = contentStr[index:sindex+1]
        switchcontentstr = contentStr[sindex+2:eindex]
        _swicth = compile('switch ({switchparam}) {')
        r = _swicth.parse(switchstr)
        assert(not r is None)
        switchparam = r['switchparam']
        blockdic = {
            'type':'switch',
            'switchparam':switchparam,
        }
        paserSwitchCaseBlock(blockdic,switchcontentstr)
        blockList.append(blockdic)
        return True
    return False

def paserIfElseBlock(blockList, contentStr):
    index = contentStr.find('if')
    if index!=-1:
        rbindex = contentStr.find(')',index+1)
        ifparam = contentStr[index+4:rbindex]
        bindex = contentStr.find('{',index+1)
        ifcontentList = []
        elsecontentList = []
        if bindex!=-1:
            pass
            #sindex, eindex = Find_matching_brackets(bindex, contentStr, '{','}')
            #ifContent = contentStr[sindex+1:eindex]
        else:
            enterindex = contentStr.find('\n',index+1)
            endenterindex = contentStr.find('\n',enterindex+1)
            ifcontent = contentStr[enterindex+1:endenterindex].strip()
            ifcontentList.append({
                'type':'normal',
                'content':ifcontent
                })
            elseindex = contentStr.find('else',index+1)
            if elseindex!=-1:
                elsebindex = contentStr.find('{',elseindex+1)
                if elsebindex!=-1:
                    pass
                else:
                    pass
            else:
                pass
        blockdic = {
            'ifparam':ifparam,
            'ifcontentList':ifcontentList,
        }
        blockList.append(blockdic)

def paserBlock(blockList, contentStr):
    if not parseSwitchBlock(blockList, contentStr):
        paserIfElseBlock(blockList, contentStr)

def paserFunctionBody(funcdic, funcContentStr):
    blockList = []
    funcdic['blockList'] = blockList
    paserBlock(blockList, funcContentStr)

def paserMemberFunction(classdic, classContentStr):
    memberFunctions=[]
    classdic['memberFunctions'] = memberFunctions
    classContentStrLines = classContentStr.split('\n')
    skiplineCount = 0
    for line in classContentStrLines:
        if skiplineCount>0:
            skiplineCount -= 1
            continue
        r = _MemberFunction.parse(line)
        if not r is None:
            #"    {visibility} {returntype} {funcname}({param}) {"
            visibility = r['visibility']
            returntype = r['returntype']
            funcname = r['funcname']
            param = r['param']
            funcdic = {
                'visibility':visibility,
                'returntype':returntype,
                'funcname':funcname,
            }
            paserParams(funcdic, param)
            memberFunctions.append(funcdic)
            #把函数拼出来
            fn = f'{funcname}({param})'
            fnindex = classContentStr.find(fn)
            assert(fnindex!=-1)
            sindex, eindex = Find_matching_brackets(fnindex, classContentStr, '{','}')
            funcContentStr = classContentStr[sindex+1:eindex]
            #print(funcContentStr)
            paserFunctionBody(funcdic, funcContentStr)
            skiplineCount = len(funcContentStr.split('\n'))


def paserClassContent(classdic, classContentStr):
    paserMemberVariables(classdic, classContentStr.split('\n'))
    paserMemberFunction(classdic, classContentStr)

def paserClass(classdefineStr, classContentStr):
    r = _class.parse(classdefineStr)
    classname = ''
    if not r is None:
        classname = r['classname']
    else:
        r = _classNoBase.parse(classdefineStr)
        if not r is None:
            classname = r['classname']
    
    classdic = { 'classname':classname,}
    paserClassContent(classdic, classContentStr)
    return classdic

def strWriteLine(s, sin):
    return s + sin +'\n'

def toLua(classdicList):
    s = ''
    s =strWriteLine(s, 'local _G, class = _G, class')
    s =strWriteLine(s, 'local g_Env = g_Env')
    s =strWriteLine(s, 'local print, tostring, SysDefines, typeof, Destroy, LogE, coroutine,string =')
    s =strWriteLine(s, '      print, tostring, SysDefines, typeof, Destroy, LogE, coroutine,string')
    s =strWriteLine(s,'_ENV = moduledef { seenamespace = CS }')
    s =strWriteLine(s,'---------------------')
    for classdic in classdicList:
        classname = classdic['classname']
        s =strWriteLine(s,f'\n{classname} = class()\n')
        #s =strWriteLine(s,f'function {classname}:__init()')

        #s =strWriteLine(s,f'end\n')
        memberFunctions = classdic['memberFunctions']
        if not memberFunctions is None:
            for funcdic in memberFunctions:
                funname = funcdic['funcname']
                paramList = funcdic['paramList']
                param = ''
                for index, paramdic in enumerate(paramList):
                    add = ','
                    if index==len(paramList)-1:
                        add = ''
                    param = param + paramdic['name'] + add

                s =strWriteLine(s,f'function {classname}:{funname}({param})')

                s =strWriteLine(s,f'end\n')

    return s
    


def main():
    # global resultStr
    # for index, line in enumerate(lines):
    #     resultStr += process(index,line, lines)
    classdicList = []
    classindex = allfileText.find('class')
    if classindex!=-1:
        sindex, eindex = Find_matching_brackets(classindex, allfileText, '{','}')
        assert(eindex!=-1)
        classdefineStr = allfileText[classindex:sindex+1]
        classContentStr = allfileText[sindex:eindex]
        
      #  print(classdefineStr+'\n\n')
      #  print(classContentStr)
        classdic = paserClass(classdefineStr, classContentStr)
        

        classdicList.append(classdic)


    print(toLua(classdicList))

main()

# if isPrintResult:
#     print(resultStr)


# if printToFile:
#     fout = open(exprotPath+'/export_'+filename.replace('.h','.cpp')+'', 'w')
#     sys.stdout = fout
# print('#include "export_BaseCore.h"\n#include"base/BaseCore.h"\n')
# print(cppfileStr)








