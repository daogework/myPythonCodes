from parse import compile
import sys
orig_stdout = sys.stdout

p = compile("[{time}  LOG_DEBUG:]:  =**TableID:{TableID} Send SUB_S_TYPESCROLL gameID:{gameID} nAllFreeCount:{nAllFreeCount} userScore:{userScore} llCurWinScore:{llCurWinScore} lincCount:{lincCount} betScore:{betScore}**=")

fout = open('H:/out.txt', 'w')
sys.stdout = fout

total = 0
scoreList = []
path = "H:/19120110.log.txt"
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()
for line in lines:
    r = p.parse(line)
    if not r is None:
        print(r)
        llCurWinScore = int(r['llCurWinScore'])
        total+=llCurWinScore
        scoreList.append(llCurWinScore)

path = "H:/19120111.log.txt"
file = open(path,mode='r', encoding="utf-8")
lines = file.readlines()
for line in lines:
    r = p.parse(line)
    if not r is None:
        print(r)
        llCurWinScore = int(r['llCurWinScore'])
        total+=llCurWinScore
        scoreList.append(llCurWinScore)



scoreList.sort(reverse=True)
print("得分排序结果:")
print(scoreList)
print("统计结果:")
print(total)



