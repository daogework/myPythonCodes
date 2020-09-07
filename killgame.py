import win32gui
import win32process
import win32api
import win32con
import subprocess 
import time
hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)
 
killname = input("输入要结束的游戏名称:")
isFound = False
 
for h,t in hwnd_title.items():
	if t is not "":
		if killname.upper() in t.upper():
			#print(h, t)
			threadpid, pid = win32process.GetWindowThreadProcessId(h)
			mypyproc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
			procname = win32process.GetModuleFileNameEx(mypyproc, 0)
			if "gameserver.exe".upper() in procname.upper():
				print("进程名:"+procname+" 窗口名:"+t)
				pro = subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i"%pid) 
				time.sleep(1)
				pro.kill()
				isFound = True
				
if not isFound:
	print("未找到进程")
			
print("任务完成，5秒后退出")
time.sleep(5)
exit()

#if __name__ == "__main__":
#	print("test")