from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
NAME = re.compile(r'[0,1,2,3,4,5,6,7,8,9]')

class UserManager(models.Manager):
	def login(self, username, password):
		activeU = self.filter(username__iexact = username)
		#  gets return a list
		if activeU and bcrypt.hashpw(password.encode("utf-8") , activeU[0].password.encode("utf-8")) == activeU[0].password:
			#should be classified as a succesful login
			return (True, activeU[0])
		else:
			return(False, {"login" : "login failed, please try again"})

	def register(self,first_name, username, password, confirm_password, datehired):
		# we want to verify all the info and make sure that the user hasn't been registered. <-- all of which cause errors!
		errors = {}

		if len(first_name) <3 :
			errors['first_name'] = "First Name is too short"
		if NAME.match(first_name):
			errors['name1'] = "First name cannot contain number(s)"
		if len(username) <3 :
			errors['username'] = "Last Name is too short"
		if len(password) < 8 :
			errors['password'] = "Password is too short"
		if password != confirm_password:
			errors['confirm_password'] = "Password must match"
		if datehired == "":
			errors['datehired'] = "Please fill in your hired date"

		if self.filter(username__iexact = username):
			errors['invalid'] = "Invalid registration, username already existed"

		

		if errors:
			return (False, errors)
		else:
		#register this person!
			hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
			self.create(first_name = first_name, username = username, password = hash_password, datehired = datehired)
			return (True, self.filter(username = username)[0])

class WishlistManager(models.Manager):
	def createitem(self, adduser, item):
		errors = {}

		if len(item) < 3:
			errors['item'] = "Item name must be longer than 3 characters"
		if item == "":
			errors['item2'] = "Item field cannot be empty"

		if errors:
			return (False, errors)
		else:
			self.create(adduser = adduser, item = item)
			return (True, "true")

	def joinlist(self, joindude, itemid):
		try:
			the_item = Wishlist.wishlistManager.get(id = itemid)
			the_item.joinuser.add(joindude)
			print the_item.joinuser
			the_item.save()
			return(True, 'true')
		except:
			return	(False, 'false')

	def removeitem(self, remover, itemid):
		try:
			remove_item = Wishlist.wishlistManager.get(id = itemid)
			test = remove_item.joinuser.remove(remover)
			print remove_item.joinuser.all()
			result = {"error": "Successfully remove item from your wishlist"}
			return (True, result )
		except:
			result = {"error": "something went wrong!"}
			return (False, result)
			
	def deleteitem(self, adduser, itemid):
		try: 
			del_item = Wishlist.wishlistManager.get(adduser = adduser, id = itemid).delete()
			return (True, 'true')
		except:
			return (False, 'false')


class User(models.Model):
	first_name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=255)
	datehired = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()
	objects = models.Manager()

class Wishlist(models.Model):
	adduser = models.ForeignKey(User, related_name = "whoadd")
	joinuser = models.ManyToManyField(User)
	item = models.CharField(max_length = 45)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	wishlistManager = WishlistManager()

	def joiner(self):
		return ",".join([str(name.first_name) for name in self.joinuser.all()])

