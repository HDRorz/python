#
#saraba1st在线脚本
#半小时登陆一次
#
#作者: HDRorz
#
#环境：Python2.7
#
#使用
#修改最下面
#def main():
#	saraba1stRobot=Robot('username','password')
#里的username和password
#

from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib
import datetime
import time
class Robot(SGMLParser):
	def __init__(self,username,password):
		SGMLParser.__init__(self)
		self.h3=False
		self.h3_is_ready=False
		self.div=False
		self.h3_and_div=False
		self.a=False
		self.depth=0
		self.names=""
		self.dic={}

		self.fastloginfield="username"
		self.username=username
		self.password=password
		self.quickforward="yes"
		self.handlekey="ls"
		try:
			cookie=cookielib.CookieJar()
			cookieProc=urllib2.HTTPCookieProcessor(cookie)
		except:
			raise
		else:
			opener=urllib2.build_opener(cookieProc)
			urllib2.install_opener(opener)

	def login(self):
		print 'Beginning connect'
		url='http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
		postdata={
			'fastloginfield':self.fastloginfield,
			'username':self.username,
			'password':self.password,
			'quickforward':self.quickforward,
			'handlekey':self.handlekey
		}
		req=urllib2.Request(
			url,
			urllib.urlencode(postdata)
		)

		self.file=urllib2.urlopen(req).read()
		tempPos=self.file.index(r'<strong class="vwmy">')
		if tempPos>1:
			temp=self.file[tempPos+21:tempPos+200]
			idStart=temp.index(r'">')
			idEnd=temp.index(r'</a>')
			self.id=temp[idStart+2:idEnd]
			print self.id
			#print temp
			print 'login success'
		else:
			print 'login fail'

def main():
	saraba1stRobot=Robot('username','password')
	while True:
		try:
			saraba1stRobot.login()
			time.sleep(1800)
		except BaseException, e:
			print e
			
if __name__ == '__main__':
	main()
			