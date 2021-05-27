from django.db import models
from django.contrib.auth.models import User 		# imports user from the django database
from django.dispatch import receiver 				# Command for django to receive TOOLS
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up	# from the library of allauth from django, you import user_signer up signals for google SIGNAL
from django.conf import settings
from datetime import datetime  
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.urls import reverse


"""
*  REFERENCES
*  Title: Django-Blog Tutorial
*  Author: Corey M Schafer
*  Date: 2018
*  URL: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*
*
*  Title: DStep by Step guide to add friends with Django
*  Author: Abhik
*  Date: October 2020
*  URL: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
*
*  Title: User Registration in Django using Google OAuth
*  Author: Section website
*  Date: December 2020
*  URL: https://www.section.io/engineering-education/django-google-oauth/
*
"""

class Profile(models.Model):
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	name = models.CharField(default=None, max_length=255, null=True)

	email = models.CharField(default=None, max_length=500, null=True)

	image = models.ImageField(default='media/default.jpg', upload_to='profile_pics')

	bio = models.CharField(default='Click Edit Profile to write your bio!', max_length=255, null=True, blank=True)

	birthday = models.DateField(default=date.today(), blank=True)

	graduation_year = models.BigIntegerField(default=2022)

	gender = models.CharField(default='No Gender Specified Yet', max_length=255, null=True, blank=True)

	my_car_status = models.CharField(default='No Car Status Specified Yet', max_length=255, null=True, blank=True)

	noise_level = models.BigIntegerField(default=5)

	location = models.CharField(default='No Location Specified Yet', max_length=255, null=True, blank=True)



	budget = models.BigIntegerField(default=500)

	friends = models.ManyToManyField("Profile", blank=True)

	

	minimum_age = models.BigIntegerField(default=18)

	maximum_age = models.BigIntegerField(default=30)
	
	budget_low = models.BigIntegerField(default=0)

	budget_high = models.BigIntegerField(default= 1000)

	noise_minimum = models.BigIntegerField(default= 1)

	noise_maximum = models.BigIntegerField(default= 10)

	preferred_gender = models.CharField(default=None, max_length=255, null=True, blank=True)

	location_preference = models.CharField(default=None, max_length=255, null=True, blank=True)

	car_status = models.CharField(default=None, max_length=255, null=True, blank=True)

	chat_token = models.CharField(default=None, max_length=255, null=True, blank=True)

	chat_id = models.CharField(default=None, max_length=255, null=True, blank=True)

	graduation_year_preference = models.BigIntegerField(default=2023)

	def __str__(self):
		return f'{self.user.username} Profile'


	def create_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.created(user=instance)



	@receiver(user_signed_up) 
	def populate_profile(sociallogin, user, **kwargs): 
		user.profile = Profile()

		simonUser = User.objects.filter(username='simonUser').first().id

		Simon = Profile.objects.filter(user = simonUser).first().id


		if sociallogin.account.provider == 'google':


			user_data = user.socialaccount_set.filter(provider='google')[0].extra_data


			email = user_data['email']
			name = user_data['name']

		user.profile.email = email
		user.profile.name = name
		user.profile.save()
		user.profile.friends.add(Simon)
		user.profile.save()


class Roommate_Request(models.Model):
	from_profile = models.ForeignKey(Profile, related_name='from_profile', on_delete=models.CASCADE)
	to_profile = models.ForeignKey(Profile, related_name='to_profile', on_delete=models.CASCADE)


class Match(models.Model):
	this_profile = models.ForeignKey(Profile, related_name='this_profile', on_delete=models.CASCADE)
	with_profile = models.ForeignKey(Profile, related_name='with_profile', on_delete=models.CASCADE)
	similarity_tokens = models.BigIntegerField(default=0)
	#matches = models.ManyToManyField("Profile", blank=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='posting_pics', default='media/default_post.jpg')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('post-detail', kwargs={'pk': self.pk})
        return reverse('roommate_app:index')


