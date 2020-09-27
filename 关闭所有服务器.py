
import win32gui
import win32api
import win32con
import time


hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)



def FindAndStop(windowsName):
	print('正在关闭 '+windowsName)
	window=win32gui.FindWindow(None,windowsName)
	if window is None:
		print(windowsName+' 未找到')
		return
	win32api.PostMessage(window, win32con.WM_CHAR, 83, 0)
	win32api.PostMessage(window, win32con.WM_CHAR, 84, 0)
	win32api.PostMessage(window, win32con.WM_CHAR, 79, 0)
	win32api.PostMessage(window, win32con.WM_CHAR, 80, 0)
	win32api.PostMessage(window, win32con.WM_CHAR, 13, 0)
	print('关闭成功 '+windowsName)
for i in range(2):
	for hwnd,t in hwnd_title.items():
		if t is not "":
			if 'Z1_' in t:
				FindAndStop(t)
	FindAndStop('Router')
	time.sleep(2)

# print('全部完成 5秒后自动关闭')
# time.sleep(5)



