import os

basepath = "G:/镜头拆解"

sortlist = []

for lists in os.listdir(basepath):
    path = os.path.join(basepath, lists)
    sortlist.append(path)

sortlist.sort(reverse=True)

for path in sortlist:
    (filepath,tempfilename) = os.path.split(path)
    (filename,extension) = os.path.splitext(tempfilename)
    print(filename)
    int_value = int(filename)
    int_value+=1
    newname = filepath+'/'+str(int_value)+extension
    print(newname)
    os.rename(path, newname)