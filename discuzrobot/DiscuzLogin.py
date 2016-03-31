# coding=utf-8
# #
# #Discuz在线脚本
# #9分钟登陆一次
# #
# #作者: HDRorz
# #
# #环境: Python2.7
# #
# #使用: python DiscuzLogin http://bbs.*.com/ username password
# #
# #
# #

from sgmllib import SGMLParser
import sys, urllib2, urllib, cookielib
import datetime
import time


class Robot(SGMLParser):
    def __init__(self, base, username, password):
        SGMLParser.__init__(self)
        self.h3 = False
        self.h3_is_ready = False
        self.div = False
        self.h3_and_div = False
        self.a = False
        self.depth = 0
        self.names = ""
        self.dic = {}

        self.base = base
        self.fastloginfield = "username"
        self.username = username
        self.password = password
        self.quickforward = "yes"
        self.handlekey = "ls"
        try:
            cookie = cookielib.CookieJar()
            cookieProc = urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)

    def login(self):
        # print 'Beginning connect'
        url = self.base + '/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
        postdata = {
            'fastloginfield': self.fastloginfield,
            'username': self.username,
            'password': self.password,
            'quickforward': self.quickforward,
            'handlekey': self.handlekey
        }
        req = urllib2.Request(
                url,
                urllib.urlencode(postdata)
        )

        self.file = urllib2.urlopen(req).read()
        tempPos = self.file.index(r'<strong class="vwmy">')
        if tempPos > 1:
            temp = self.file[tempPos + 21: tempPos + 200]
            idStart = temp.index(r'">')
            idEnd = temp.index(r'</a>')
            self.id = temp[idStart + 2: idEnd]
            # print self.id
            # print temp
            # print 'login success'

            hashPos = self.file.index(r'name="formhash"')
            if hashPos:
                hash = self.file[hashPos - 10: hashPos + 40]
                hashStart = hash.index(r'value="')
                self.formhash = hash[hashStart + 7: hashStart + 15]
                # print 'formhash'
                # print self.formhash

            return True
        else:
            print 'login fail'
            return False

    def applytask(self):
        # print 'Applying task'
        url = self.base + 'home.php?mod=task&do=apply&id=14'
        req = urllib2.Request(url)
        self.file = urllib2.urlopen(req).read()
        # print 'apply success'
        return True

    def postreply(self):
        # print 'Replying'
        url = self.base + '/forum.php?mod=post&action=reply&fid=161&tid=2254131&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
        postdata = {
            'message': '刷个日常',
            'formhash': self.formhash,
            'usesig': 1
        }
        req = urllib2.Request(url, urllib.urlencode(postdata))
        self.file = urllib2.urlopen(req).read()
        # print self.file

        # print 'reply success'
        return True

    def draw(self):
        # print 'drawing'
        url = self.base + '/home.php?mod=task&do=draw&id=14'
        req = urllib2.Request(url)
        self.file = urllib2.urlopen(req).read()
        # print self.file

        # print 'draw success'
        return True

    def sign(self):
        # print 'Signing'
        url = self.base + '/plugin.php?id=mpage_sign:sign&inajax=1'
        postdata = {
            'formhash': self.formhash,
            'signsubmit': 'yes',
            'handlekey': 'sign',
            'moodid': 1,
            'content': '记上一笔，hold住我的快乐！',
        }
        req = urllib2.Request(url, urllib.urlencode(postdata))
        self.file = urllib2.urlopen(req).read()
        # print self.file

        # print 'sign success'
        return True


def main(base, username, password):
    DiscuzLogin = Robot(base, username, password)
    while True:
        try:
            DiscuzLogin.login()
            time.sleep(500)
        except BaseException, e:
            print e


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
