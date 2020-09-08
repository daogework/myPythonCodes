import pyodbc
import subprocess 
import os
import time


#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER="117.78.27.84";DATABASE=QPPlatformDB;UID=me;PWD=pass')
cnxn = pyodbc.connect(
DRIVER="{SQL Server}",
SERVER="117.78.27.84",
DATABASE='QPPlatformDB',
UID='aaaaaa',PWD='aaaaaa')

cursor = cnxn.cursor()
cursor.execute("SELECT ServerName,ServerID,KindID FROM GameRoomInfo WHERE ServiceMachine = '9FCC68B5BC258EE10F30BF49BDE8AA41'")

gameDic = dict()
gameKindDic = dict()

while True:
	row = cursor.fetchone()
	if not row:
		break
	print('ServerName:', row.ServerName, 'ServerID:', row.ServerID,'KindID:', row.KindID)
	gameDic.update({row.ServerID:row.ServerName})
	gameKindDic.update({row.ServerID:row.KindID})
	
cnxn.close() 

isFound = False
tagetGame=''
while True:
	tagetGame = input("输入要启动的游戏名称或房间ID或者.KindID（输入*游戏名可筛选）:")
	if '*' in tagetGame:
		print('------------------------------------------------------------')
		tagetGame=tagetGame.replace('*','')
		for ServerID,ServerName in gameDic.items():
			if tagetGame in ServerName:
				print('ServerName:', ServerName, 'ServerID:', ServerID)
	else:
		break
path = "D:\\Unicode"
print("\n\n")

if tagetGame.isdigit():
	tagetGameID = int(tagetGame)
	for ServerID,ServerName in gameDic.items():
		if ServerID == tagetGameID:
			isFound = True
			print("@@@找到的房间名:"+ServerName+" ID:"+str(ServerID))
			pro = subprocess.Popen(""+path+"\\GameServer.exe /ServerID:"+str(ServerID) , shell=True)
			time.sleep(1)
			pro.kill()
else:
	if '.' in tagetGame:
		kindID = tagetGame[1:]
		tagetGame = "KindID:"+kindID
		for ServerID,KindID in gameKindDic.items():
			if int(kindID) == KindID:
				isFound = True
				print("@@@找到的房间名:"+gameDic[ServerID]+" ID:"+str(ServerID))
				pro = subprocess.Popen(""+path+"\\GameServer.exe /ServerID:"+str(ServerID) , shell=True)
				time.sleep(1)
				pro.kill()
	else:
		for ServerID,ServerName in gameDic.items():
			if tagetGame in ServerName:
				isFound = True
				print("@@@找到的房间名:"+ServerName+" ID:"+str(ServerID))
				pro = subprocess.Popen(""+path+"\\GameServer.exe /ServerID:"+str(ServerID) , shell=True)
				time.sleep(1)
				pro.kill()
		
if not isFound:
	print("未找到游戏 tagetGame:"+tagetGame)
	
print("任务完成，5秒后退出")
time.sleep(5)
exit()


#if __name__ == "__main__":
#	print("test")