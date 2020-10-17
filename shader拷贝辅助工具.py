from parse import compile
from parse import findall
import sys
import os
import time

import pyperclip
from pymsgbox import alert


outputpath = r"H:\UnityTestProject\resexport3\Assets\shaders" + '/'


_paser = compile('Shader "{shadername}"{}') 


_lastText = ''

while True:
    text = pyperclip.paste()
    if text=='_exit':
        break
    if _lastText!=text:
        _lastText = text
        r = _paser.parse(text)
        if not r is None:
            shadername = r['shadername']
            filename = shadername.replace('/',' ')
            f = open(outputpath+filename+'.shader', 'w')
            f.write(text)
            f.flush()
            f.close()
            print('wrote file '+filename)
            alert(text='文件名'+filename, title='完成', button='OK')

    time.sleep(0.05)


