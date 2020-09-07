import codecs

def is_zh ( c):
    x = ord ( c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

    # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

    # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

    # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

    # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True

    else:
         return False

f = codecs.open("./缅语收集.txt",'r','utf-8')
lines = f.readlines()

fw=codecs.open("./mydict.txt","w","utf-8")

for line in lines:
    s1 = ""
    s2 = ""
    # for idx, s in enumerate(line):
    #     if is_zh(s):
    #         s1+=s
    #     else:
    #         s2+=s
    for idx, s in enumerate(line):
        if is_zh(s):
            s1 = line[idx:len(line)].replace('\r', '').replace('\n', '')
            s2 = line[0:idx]
            break

    if len(s1)!=0:
        print(s1+"@"+s2)
        fw.write(s1+"@"+s2+'\n')
    
f.close()
fw.close()