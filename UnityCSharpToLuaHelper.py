from parse import compile
from parse import findall
import sys

orig_stdout = sys.stdout

_using= compile("{}using{};")
_using2= compile("using{};")
_class= compile("public class {classname} : {classbasename} {")
_class2= compile("public class {classname} {")
_public_func= compile("{space}public {returntype} {funcname}() {")
_public_funcpara= compile("{space}public {returntype} {funcname}({param}) {")
_private_func= compile("{space}private {returntype} {funcname}() {")
_private_funcpara= compile("{space}private {returntype} {funcname}({param}) {")
_protected_func= compile("{space}protected {returntype} {funcname}() {")
_protected_funcpara= compile("{space}protected override {returntype} {funcname}({param}) {")
_protectedov_func= compile("{space}protected override {returntype} {funcname}() {")
_protectedov_funcpara= compile("{space}protected {returntype} {funcname}({param}) {")
_ctor= compile("{space}public {ctor}() {")
_ctorparam= compile("{space}public {ctor}({param}) {")
_var_1= compile("{space}var {v1} = {v2};")
_v_1= compile("        {v1} = {v2};")
__findlist= compile("{}new List<{Type}>()")
_private_member= compile("{space}private {type} {member_name} = {value};")
_public_member= compile("{space}public {type} {member_name} = {value};")
_public_member_empty= compile("{space}public {type} {member_name};")
_get_set = compile("{space}public {type} {value_name} {")

_msgcenter_event = compile("{space}MessageCenter.Instance.{}({}, {callbackfunc});")

fout = open('H:\\python脚本\\__fortest/out.lua', 'w')
#sys.stdout = fout

total = 0
scoreList = []
filename = 'CommonModule.cs'
rootpath = "H:\\fll3d_optimization\\client\\Plaza\\Assets\\Scripts\\GameLogic\\Module"
path = rootpath + '/' + filename
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()

resultStr = ''

isPrintResult = True

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

    r = _msgcenter_event.parse(line)
    if not r is None:
        line = line.replace('Instance.','Instance:')
        callbackfunc = r['callbackfunc']
        space=r['space']
        if 'AddListener' in line:
            oldname = 'old'+callbackfunc
            localold = space+'local '+oldname+' = '+ 'self.'+callbackfunc +'\n'
            newfunc = space+'self.'+callbackfunc+' = function(msg) '+oldname+'(self, msg) end\n'
            line = line.replace(callbackfunc,'self.'+callbackfunc)
            return localold+newfunc+line+'\n'
        else:
            line = line.replace(callbackfunc,'self.'+callbackfunc)
        return line

    r = _using.parse(line)
    r2 = _using2.parse(line)
    if not r is None or not r2 is None:
        return''
        
    r = _class.parse(line)
    if not r is None:
        classname = r['classname']
        return 'local '+classname+' = {\n'
        
    else:
        r = _class2.parse(line)
        if not r is None:
            classname = r['classname']
            return 'local '+classname+' = {\n'

 
    r = paserFunc(line, _private_func, _private_funcpara)
    if r != 'notfound':
        return r 
  
    r = paserFunc(line, _public_func, _public_funcpara)
    if r != 'notfound':
        return r  

    r = paserFunc(line, _protected_func, _protected_funcpara)
    if r != 'notfound':
        return r  

    r = paserFunc(line, _protectedov_func, _protectedov_funcpara)
    if r != 'notfound':
        return r  

    r = _ctor.parse(line)
    if not r is None:
        space=r['space']
        return space+'ctor = function(self)\n'
        
    else:
        r = _ctorparam.parse(line)
        if not r is None:
            param = r['param']
            param = paserParam(param)
            space=r['space']
            return space+'ctor = function(self,'+param+')\n'
    
    r = _var_1.parse(line)
    if not r is None:
        space = r['space']
        v1 = r['v1']
        v2 = r['v2']
        s = space+'local '+v1+' = '+v2+'\n'
        r = __findlist.parse(s)
        if not r is None:
            listtype = r['Type']
            liststr = 'new List<'+listtype+'>()'
            s=s.replace(liststr,'{}')
        return s

    r = _v_1.parse(line)
    if not r is None:
        v1 = r['v1']
        v2 = r['v2']
        s = '        self.'+v1+' = '+v2+'\n'
        r = __findlist.parse(s)
        if not r is None:
            listtype = r['Type']
            liststr = 'new List<'+listtype+'>()'
            s=s.replace(liststr,'{}')
        
        return s
    
    r = _private_member.parse(line)
    if not r is None:
        #{space}private {type} {member_name} = {value};
        member_name=r['member_name']
        value=r['value']
        space=r['space']
        return space+member_name+' = '+value+'\n'
    r = _public_member.parse(line)
    if not r is None:
        member_name=r['member_name']
        value=r['value']
        space=r['space']
        return space+member_name+' = '+value+'\n'
    r = _public_member_empty.parse(line)
    if not r is None:
        return ''
    r = _get_set.parse(line)
    if not r is None:
        #{space}public {type} {value_name} {
        space = r['space']
        value_name = r['value_name']
        passCount = count_get_set_line(index, lines)
        getstr = find_get(index+1, lines)
        setstr = find_set(index+1, lines, value_name)
        return space+value_name+' = {\n' + getstr + setstr+space+'}\n'
    if line.startswith('    }'):
        return '    end,\n'
    return line

def count_get_set_line(index, lines):
    counter = 0
    lineCounter = 0
    isFoundFirst = False
    for lineindex in range(index,len(lines)):
        
        line = lines[lineindex]
        if '{' in line:
            isFoundFirst = True
            counter+=1
        if '}' in line:
            isFoundFirst = True
            counter-=1
        if isFoundFirst and counter==0:
            break
        lineCounter+=1
        
    return lineCounter

def find_end_of_parantheses(index, lines):#寻找 }
    str = ''
    for lineindex in range(index,len(lines)):
        line = lines[lineindex]
        str+=line
        if '}' in line:
            break
    return str

def find_get(index, lines):
    for lineindex in range(index,len(lines)):
        line = lines[lineindex]
        if 'get' in line:
            getstr = find_end_of_parantheses(lineindex, lines)
           # getstr = getstr.replace('\n',' ')
            getstr = getstr.replace('get','get = function(self)')
            getstr = getstr.replace('{','')
            getstr = getstr.replace('}','end')
            getstr = getstr.replace(';','')
            getstr = getstr.replace('return ','return self.')
            return getstr
    return ''

def find_set(index, lines, setfieldname):
    head = setfieldname[0]
    setfieldname = setfieldname.replace(head, head.lower())
    for lineindex in range(index,len(lines)):
        line = lines[lineindex]
        if 'set' in line:
            setstr = find_end_of_parantheses(lineindex, lines)
            #setstr = setstr.replace('\n','**')
            setstr = setstr.replace('set','set = function(self)')
            setstr = setstr.replace('{','')
            setstr = setstr.replace('}','end')
            setstr = setstr.replace(';','')
            #setstr = setstr.replace('**','\n')  
            setstr = setstr.replace(setfieldname,'self.'+setfieldname)
            return setstr
    return ''
        
    
def paserFunc(line, paser, paserparam):
    r = paser.parse(line)
    if not r is None:
        space=r['space']
        funcname = r['funcname']
        return space+funcname+' = function(self)\n'
    else:
        r = paserparam.parse(line)
        if not r is None:
            space=r['space']
            funcname = r['funcname']
            param = r['param']
            param = paserParam(param)
            return space+funcname+' = function(self,'+param+')\n'  
    return 'notfound'

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)
    
    resultStr = resultStr.replace(';','')


main()

if isPrintResult:
    print(resultStr)







