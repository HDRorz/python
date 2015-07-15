#coding=utf-8 
import Tkinter
import tkMessageBox
import os
from subprocess import Popen

class TkButtonDemo:
	def __init__(self):
		self.top = Tkinter.Tk()
		self.top.title(u'按钮demo')
		self.top.geometry('500x500')
		#self.iconbitmap('root')
		
		self.button1 = Tkinter.Button(self.top, text=u'任务1', command=self.Button1Click)
		self.button1.pack()
		
	def Button1Click(self):
		b1cmd = r'cmd /min E:\大二\大二第一学期\C++\0.0.exe'
		#result = os.system(b1cmd)
		#result = os.system(u'start E:\大二\大二第一学期\C++\0.0.exe')
		process = Popen(b1cmd)
		tkMessageBox.showinfo(u'提示', u'任务已完成')



def main():
	obj = TkButtonDemo()
	Tkinter.mainloop()		
	
if __name__ == '__main__':
	main()