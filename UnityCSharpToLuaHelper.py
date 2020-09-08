from parse import compile
import sys

orig_stdout = sys.stdout

_using= compile("{}using{};")
_using2= compile("using{};")
_class= compile("public class {classname} : {classbasename} {")
_class2= compile("public class {classname} {")
_ctor= compile("{}public {ctor}() {")
_ctorparam= compile("{}public {ctor}({param}) {")
_v_1= compile("        {v1} = {v2};")
__findlist= compile("{}new List<{Type}>()")



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

def process(index, line):
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
            
    r = _ctor.parse(line)
    if not r is None:
        return '    ctor = function(self)\n'
        
    else:
        r = _ctorparam.parse(line)
        if not r is None:
            param = r['param']
            param = paserParam(param)
            return '    ctor = function(self,'+param+')\n'
            
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
    if line=='    }':
        return '    end'
    return line

for index, line in enumerate(lines):
    resultStr += process(index,line)

    

if isPrintResult:
    print(resultStr)







