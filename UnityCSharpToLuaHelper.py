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
__findlist= compile("{}new List<{Type}>();")
_private_member= compile("{space}private {type} {member_name} = {value};")
_public_member= compile("{space}public {type} {member_name} = {value};")
_public_member_empty= compile("{space}public {type} {member_name};")
_get_set = compile("{space}public {type} {value_name} {")
_lambda_param = compile("{}(({param}) => {")

_msgcenter_event = compile("{space}MessageCenter.Instance.{}({}, {callbackfunc});")
_ReferenceEquals = compile("{}ReferenceEquals({value}, null){}")


#fout = open('H:\\python脚本\\__fortest/out.lua', 'w')
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

    r = _lambda_param.parse(line)
    if not r is None:
        passCount = count_get_set_line(index, lines)
        lambdastr = find_end_of_parantheses(index, lines)
        param = r['param']
        lambdkeyastr = '('+param+') => {'
        funcstr = 'function('+param+')'
        lambdastr = lambdastr.replace(lambdkeyastr,funcstr)
        k = lambdastr.rfind("}")
        lambdastr = lambdastr[:k] + "end" + lambdastr[k+1:]
        return lambdastr
    
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
        space = ''
        for b in line:
            if b==' ':
                space+=b
            else:
                break
        v1 = r['v1']
        v2 = r['v2']
        s = 'self.'+v1+'='+v2+'\n'
        s = s.replace(' ','')
        s = s.replace('=',' = ')
        r = __findlist.parse(line)
        if not r is None:
            listtype = r['Type']
            liststr = 'newList<'+listtype+'>()'
            s=s.replace(liststr,'{}')
        
        return space+s
    
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
    
    r = _ReferenceEquals.parse(line)
    if not r is None:
        value = r['value']
        originalstr = 'ReferenceEquals('+value+', null)'
        newstr = '('+value+'==nil)'
        line = line.replace(originalstr, newstr)
        return line

    if line.startswith('    }'):
        return '    end,\n'
    return line

def count_get_set_line(index, lines):
    counter = 0
    lineCounter = 0
    isFoundFirst = False
    for lineindex in range(index,len(lines)):
        line = lines[lineindex]
        for s in line:
            if s=='{':
                counter+=1
                isFoundFirst = True
        for s in line:
            if s=='}' and isFoundFirst:
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


def replaceByIndex(s, index, newstring):
     return s[:index] + newstring + s[index + 1:]

def fine_end_of_start_end(index, rstr, start, end):#找到括号尾部index
    count = 0
    isFoundFirst = False
    for i in range(index,len(rstr)):
        s = rstr[i]
        if s==start:
            count+=1
            isFoundFirst = True
        elif s==end and isFoundFirst:
            count-=1
        if count==0 and isFoundFirst:
            return i
    return -1

def fine_end_of_start_end2(index, rstr, start, startlen, end):#找到括号尾部index
    count = 0
    isFoundFirst = False
    for i in range(index,len(rstr)):
        s = rstr[i]
        startstr = rstr[i:i+startlen]
        if startstr==start:
            count+=1
            isFoundFirst = True
        elif s==end and isFoundFirst:
            count-=1
        if count==0 and isFoundFirst:
            return i
    return -1
    
def iscontinueWith(startindex,rstr, char):
    for i in range(startindex, len(rstr)):
        s = rstr[i]
        if s==' ' or s=='\n':
            continue
        elif s==char:
            return True
        else:
            break
    return False

def handleIfElse(rstr):
    willreplcacetoendlist = []
    index = rstr.find('if')
    while index != -1:
        index+=2
        
        bindex = fine_end_of_start_end(index, rstr,'(',')')
        rstr = replaceByIndex(rstr, bindex, ') then')
        index = rstr.find('if', bindex)
        
    index = rstr.find('else')
    while index != -1:
        if iscontinueWith(index+4, rstr, '{'):
            bindex = fine_end_of_start_end(index, rstr,'{','}')
            assert(bindex!=-1)
            willreplcacetoendlist.append(bindex)
            index = rstr.find('else', index+1)
        else:
            index = rstr.find('else', index+1)

    index = rstr.find('then')
    while index != -1:#思路 找到then后面的括号匹配,难点：有点then后面没有括号，要排除
        if iscontinueWith(index+4, rstr, '{'):
            bindex = fine_end_of_start_end(index, rstr,'{','}')
            assert(bindex!=-1)
            if rstr[bindex+1]=='\n':
                willreplcacetoendlist.append(bindex)
            index = rstr.find('then', index+1)
        else:
            index = rstr.find('then', index+1)

    for index in willreplcacetoendlist:
        rstr = replaceByIndex(rstr, index, '#')

    rstr = rstr.replace('else {','else')
    rstr = rstr.replace(' then {',' then')
    rstr = rstr.replace('} else','else')
    rstr = rstr.replace('#','end ')

    return rstr

def main():
    global resultStr
    for index, line in enumerate(lines):
        resultStr += process(index,line, lines)
    
    resultStr = resultStr.replace(';','')
    resultStr = resultStr.replace('//','--')
    resultStr = resultStr.replace('.ToString()',':ToString()')
    resultStr = resultStr.replace('new ','')
    resultStr = resultStr.replace(' && ',' and ')
    resultStr = resultStr.replace(' != ',' ~= ')
    resultStr = resultStr.replace('!(','not(')
    
    resultStr = resultStr.replace('else if','elseif')

    resultStr = handleIfElse(resultStr)

    #resultStr = resultStr.replace(' then {',' then')
    
    



main()

if isPrintResult:
    print(resultStr)







