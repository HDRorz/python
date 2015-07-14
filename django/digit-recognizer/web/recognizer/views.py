#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.contrib import messages
from django import forms
from django.conf import settings
import time
from datetime import datetime
import functools
from models import Users
from collections import namedtuple
import random
import pytz
import json

#并没有什么卵用
def get_datetimenow():
	AsiaShanghaiTZ = pytz.timezone(settings.TIME_ZONE)
	return AsiaShanghaiTZ.localize(datetime(*time.localtime()[:6]))

#
def login_required(func):
	@functools.wraps(func)
	def newfunc(request, *args, **kargs):
		if not request.user.is_authenticated():
			messages.warning(request, u"你尚未登录，登录后可使用此项功能")
			return HttpResponseRedirect(settings.ROOTPATH)
		return func(request, *args, **kargs)
	return newfunc

#register页面处理
def user_register(request):
	curtime=get_datetimenow();
	
	if request.user.is_authenticated():
		return HttpResponseRedirect("/register/")
	try:
		if request.method=='POST':
			username=request.POST.get('username','')
			password1=request.POST.get('password1','')
			password2=request.POST.get('password2','')
			email=request.POST.get('email','')
			nickname=request.POST.get('nickname','')
			errors=[]
			
			registerForm=RegisterForm({'username':username,'password1':password1,'password2':password2,'email':email,'nickname':nickname})
			if not registerForm.is_valid():
				errors.extend(registerForm.errors.values())
				return render(request,"register.html",{'curtime':curtime,'username':username,'email':email,'nickname':nickname,'errors':errors})
			if password1!=password2:
				errors.append(u"两次输入的密码不一致!")
				return render(request,"register.html",{'curtime':curtime,'username':username,'email':email,'nickname':nickname,'errors':errors})
				
			filterResult=Users.objects.filter(username=username)#c************
			if len(filterResult)>0:
				errors.append(u"用户名已存在")
				return render_to_response("/register/",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'nickname':nickname,'errors':errors}))
			
			user=Users()
			user.username=username
			user.set_password(password1)
			user.email=email
			user.nickname=nickname
			user.save()
			newUser=auth.authenticate(username=username,password=password1)
			if newUser is not None:
				auth.login(request, newUser)
				return HttpResponseRedirect(settings.ROOTPATH)
	except Exception,e:
		errors.append(str(e))
		#这个errors会出来一堆u/什么什么的未编码utf8（
		return render(request,"register.html",{'curtime':curtime,'username':username,'email':email,'nickname':nickname,'errors':errors})
	
	#return render_to_response("/register",RequestContext(request,{'curtime':curtime}))
	return render(request,"register.html",{'curtime':curtime})

#login页面处理
def user_login(request):
	curtime=get_datetimenow()
		
	if request.method=='POST':
		print("POST")
		username=request.POST.get('username','')
		password=request.POST.get('password','')
		user= auth.authenticate(username=username,password=password)#a***********
		if user and user.is_active:
			auth.login(request, user)
			return render(request,"success.html")
	#return render_to_response("/login/",RequestContext(request,{'curtime':curtime}))
	return render(request,"login.html")

#登出页面处理
def user_logout(request):
	curtime=get_datetimenow()
	
	auth.logout(request)
	
	return HttpResponseRedirect("/login/")

#上传页面处理
def upload(request):
	curtime=get_datetimenow()
	try:
		files = request.FILES.getlist('file')
		filecount=0
		for f in files:      
			#destination = open('d:/temp/' + f.name,'wb+')
			for chunk in f.chunks():
			#可以上传上来多个文件 所以用for处理
				filecount = filecount+1
				#destination.write(chunk)
			#destination.close()
		#使用json回传数据 errors可以抛弃了（
		response_data = {}
		response_data['result'] = 'success'
		if files:
			#return render(request,"success.html")
			return HttpResponse(json.dumps(response_data), content_type="application/json")
	except Exception,e:
		response_data.append(str(e))
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return render(request,"upload.html")

#这些是原来justsoso的 看上去没有什么卵用	
# def index(request):
	# choice_questions = []
	# blank_questions = []
	# #print request.user
	# if request.user.is_authenticated():
		# choice_questions, blank_questions = get_cb_questions(request.user)
	# return render(request, "index.html", {'loginform': LoginForm()})

# def login(request):
	# form = LoginForm(request.POST)
	# if not form.is_valid():
		# messages.warning(request, u"用户名或密码不能为空")
	# else:
		# uid = form.cleaned_data['uid']
		# pwd = form.cleaned_data['pwd']

		# user = authenticate(username=uid, password=pwd)
		# if user:
			# login(request, user)
		# else:
			# messages.warning(request, u"登录失败,用户名与密码不匹配")
	# return HttpResponseRedirect(settings.ROOTPATH)

#登陆表单
class LoginForm(forms.Form):
	uid = forms.CharField(max_length=12, label=u"用户名:", widget=forms.TextInput(attrs={"class": 'span2'}))
	pwd = forms.CharField(max_length=50, label=u"密码:", widget=forms.PasswordInput(attrs={"class": 'span2'}))

#注册表单
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=12, label=u"用户名:", widget=forms.TextInput(attrs={"class": 'span2'}))
	password1 = forms.CharField(max_length=50, label=u"密码:", widget=forms.PasswordInput(attrs={"class": 'span2'}))
	password2 = forms.CharField(max_length=50, label=u"重复密码:", widget=forms.PasswordInput(attrs={"class": 'span2'}))
	#这个在高版本的django上应该可以改成emailfield、emailinput
	email = forms.CharField(max_length=50, label=u"电子邮件:", widget=forms.TextInput(attrs={"class": 'span2'}))
	nickname = forms.CharField(max_length=50, label=u"昵称:", widget=forms.TextInput(attrs={"class": 'span2'}))
	