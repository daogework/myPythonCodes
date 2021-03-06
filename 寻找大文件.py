# search File according to its size or other information

import os
import math

max_size = 1024*1024

class search():
	def __init__(self,path):
		if isinstance(path,str):
			self.__path__ = path
			self.status = os.stat(path)
			self.files_and_dirs = os.listdir(path)
		else:
			self.__path__ = '/'
			self.status = os.stat('/')
			self.files_and_dirs = os.listdir('/')
		self.__current_path__ = os.getcwd()
		self.__KB__ = 1024
		self.__MB__ = self.__KB__ * 1024
		self.__GB__ = self.__MB__ * 1024
		self.__TB__ = self.__GB__ * 1024
		self.__fileSize__ = self.__GB__ * 2
	
	def getInformation(self):
		st_mode = self.status.st_mode
		st_ino  = self.status.st_ino
		st_dev  = self.status.st_dev
		st_nlink = self.status.st_nlink
		st_uid  = self.status.uid
		st_gid  = self.status.gid
		st_size = self.statis.size
		st_atime = self.status.st_atime
		st_mtime = self.status.st_mtime
		st_ctime = self.status.st_ctime
		
		return st_mode,st_ino,st_dev,st_nlink,st_uid,st_gid,st_size,st_atime,st_mtime,st_ctime

	def sortFilesDirs(self):
		#print self.files_and_dirs
		files = []
		dirs = []
		links = []
		mounts = []
		os.chdir(self.__path__)
		for f in self.files_and_dirs:
			#print "in for, f = %s" %f
			if os.path.isfile(f):
			#	print "is file %s" %f
				files.append(f)
			elif os.path.isdir(f):
			#	print "is dir %s" %f
				dirs.append(f)
			elif os.path.islink(f):
			#	print "is link %s" %f
				links.append(f)
			elif os.path.ismount(f):
			#	print "is mount %s" %f
				mounts.append(f)
			else:
				pass
		files.sort()
		dirs.sort()
		links.sort()
		mounts.sort()
		os.chdir(self.__current_path__)
		return files,dirs,links,mounts

	def setSize(self,size):
		"""
		size: number + KB/MB/GB
		for example: "2GB+312MB+47KB"
		"""
		# if isinstance(size,str):
		# 	s = size.split('+')
		# 	l = 0
		# 	while l < 3 - len(s):	
		# 		s.append('')
		# 		l += 1
		# 	GB = s[0]
		# 	MB = s[1]
		# 	KB = s[2]
		# self.__fileSize__ = self.__GB__ * int(GB[:-2]) + self.__MB__ * int(MB[:-2]) + self.__KB__ * int(KB[:-2])

	def findBigSizeFile(self):
		files = self.sortFilesDirs()[0]
		os.chdir(self.__path__)
		sizes = []
		d = {}
		#print "filesize = %s" %self.__fileSize__
		for f in files:
			size = int(os.path.getsize(f))
			#print size
			if size > max_size:
				sizes.append(size)
				print(self.__path__+'  name:'+f,'    size:'+str(math.floor(size/1024/1024))+'MB')
			else:
				pass 
		os.chdir('.')
		#if len(sizes) > 0:
			#d = d.update({self.__path__:sizes})
			#d = {self.__path__:sizes}
		return d

def walk2Find(path,size):
	bigFileDicts = {}
	if isinstance(path,str) and isinstance(size,str) and os.path.exists(path):
		walkMachine = os.walk(path)
		for p in walkMachine:
			searchMachine = search(p[0])
			searchMachine.setSize(size)
			fileDict = searchMachine.findBigSizeFile()
			if fileDict != None and len(fileDict) > 0:
				bigFileDicts.update(fileDict)
	else:
		pass
	return bigFileDicts
			

if __name__ == '__main__':
	max_size = 90*1024*1024 #文件大小在这里设置
	bigFiles = walk2Find(r'H:\fll3d_subGames\FQZS_Lua',"")
	#for f in bigFiles:
	#	print (f)
	
	print ("success!")
