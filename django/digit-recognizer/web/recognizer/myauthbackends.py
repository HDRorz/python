#coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.contrib.auth import backends
from django.contrib.auth.models import User
from models import Users
import network
import logging
logger = logging.getLogger(__name__)

class UserDirectSignupBackend(backends.ModelBackend):
	@property
	def Users(self):
		if not hasattr(self, '_user_class'):
			self._user_class = models.get_model(*settings.CUSTOM_USER_MODEL[0].split('.', 2))
		if not self._user_class:
			raise ImproperlyConfigured("Could not get custom user model")
		return self._user_class

	def authenticate(self, username=None, password=None):
		logger.info("start auth")
		loginpage = network.getloginpageS(username, password)
		if network.NotLogin(loginpage):
			return None
		userpage = network.getuserpage()
		#logger.debug(userpage)
		pinfo = network.PersonInfo(userpage)
		#logger.debug(pinfo)
		if not pinfo.check:
			return None
		try:
			user = Users.objects.get(username__exact=dbusername)
		except Users.DoesNotExist:
			#usersettings = UserSettings()
			#usersettings.save()

			logger.debug(pinfo.name + " " + pinfo.department)
			user = Users()
			user.username    = username
			user.password    = password
			user.type        = pinfo.type
			user.nickname    = pinfo.nickname
			#user.settings    = usersettings
			user.save()
			return user
		return None

	def get_user(self, user_id):
		try:
			logger.info("user_id: %d" % user_id)
			user = User.objects.get(pk=user_id)
			user = user.userheadshu
			return user
		except ObjectDoesNotExist:
			return None
