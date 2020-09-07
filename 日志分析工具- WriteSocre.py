from parse import compile
import sys
orig_stdout = sys.stdout

strPatten = "[{time} LOG_DEBUG:]:  =**TableID:{TableID} gameID:{gameID} score:{score} level:{level} reason:{reason}**="

p = compile(strPatten)

#fout = open('H:/out.txt', 'w')
#sys.stdout = fout

total = 0
scoreList = []
path = "H:/19120217.log2.txt"
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()
for line in lines:
    r = p.parse(line)
    if not r is None:
        score = int(r['score'])
        total+=score


path = "H:/19120216.log2.txt"
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()
for line in lines:
    r = p.parse(line)
    if not r is None:
        score = int(r['score'])
        total+=score

print("统计结果:")
print(total)



